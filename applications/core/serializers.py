from rest_framework import serializers
from .models import *
from applications.accounts.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from applications.accounts.models import Profile

class EmployerCompanySerialzers(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email')

    class Meta:
        model = EmployerCompany
        fields = [
            'id',
            'user',
            'name',
            'country'
        ]

    def create(self, validated_data):
        user_email = validated_data.pop('user').get('email')
        user = User.objects.get(email=user_email)
        employercompany = EmployerCompany.objects.create(user=user, **validated_data)  # Используем **validated_data
        return employercompany


User = get_user_model()


class InvitationSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True)
    vacancy_id = serializers.PrimaryKeyRelatedField(queryset=Vacancy.objects.all(), write_only=True)
    employer_email = serializers.EmailField(source='employer.user.email')


    class Meta:
        model = Invitation
        fields = ['id', 'user_email','message', 'status', 'vacancy_id', 'employer_email']

    def get_vacancy(self, obj):
        return obj.vacancy.id

    def create(self, validated_data):

        user_email = validated_data.pop('user_email')
        employer_email = validated_data.pop('employer').get('user').get('email')
        employer = EmployerCompany.objects.get(user__email=employer_email)
        vacancy_id = validated_data.pop('vacancy_id').id  # Получаем ID вакансии
        status = validated_data.get('status')

        # Получаем пользователя-студента по Email
        try:
            user = User.objects.get(email=user_email, is_student=True, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("Student not found")


        # Получаем вакансию по ее ID
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            raise serializers.ValidationError("Vacancy not found")

        # Создаем приглашение, связанное с этими пользователями и вакансией
        invitation = Invitation.objects.create(
            user=user,
            vacancy=vacancy,
            employer=employer,
            **validated_data
        )

        # Генерируем сообщение в зависимости от статуса
        if status == 'accepted':
            message = f'Уважаемый {user.email}, приглашаем вас на собеседование в нашей компании {vacancy.name}'
        elif status == 'declined':
            message = f'Уважаемый {user.email}, ваше приглашение на собеседование в компанию {vacancy.name} было отклонено'
        else:
            message = f'Уважаемый {user.email}, вы получили приглашение на собеседование в компанию {vacancy.name}'

        invitation.message = message
        invitation.save()

        return invitation


class InvatationGetSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email')
    employer_email = serializers.EmailField(source='employer.user.email')
    
    class Meta:
        model = Invitation
        fields = ['id', 'user_email', 'message', 'status', 'vacancy', 'employer_email']


class VacancySerializers(serializers.ModelSerializer):
    employer_company = EmployerCompanySerialzers()

    class Meta:
        model = Vacancy
        fields = [
            'id',
            'language',
            'proficiency',
            'picture',
            'employer_company',
            'name',
            'salary',
            'duty',
            'city',
            'accomodation_type',
            'accomodation_cost',
            'is_vacancy_confirmed',
            'insurance',
            'transport',
            'contact_info',
            'destination_point',
            'employer_dementions',
            'extra_info',
            'is_new',
        ]

    def create(self, validated_data):
        employer_company_data = validated_data.pop('employer_company')
        employer_company_name = employer_company_data.get('name')
        employer_company_country = employer_company_data.get('country')

        user_email = employer_company_data.get('user').get('email')
        user = User.objects.get(email=user_email)

        employer_company, created = EmployerCompany.objects.get_or_create(
            name=employer_company_name, user=user, country=employer_company_country
        )

        validated_data['user'] = user  # Set the user for the Vacancy instance

        vacancy = Vacancy.objects.create(employer_company=employer_company, **validated_data)

        # Отправляем уведомление через WebSocket после успешного создания вакансии
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': 'Новая вакансия создана!'
            }
        )

        return vacancy
    
    
    def get_is_new(self, obj):
        return obj.is_new()


class VacancyFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancyChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['id', 'picture', 'name', 'salary', 'city', 'accomodation_cost', 'insurance', 'transport',
                  'contact_info', 'destination_point', 'employer_dementions', 'extra_info', 'duty',
        ]


class ReviewVacancySerializer(serializers.ModelSerializer):
    # Добавляем эти поля для обработки почтовых адресов
    applicant_profile_email = serializers.EmailField(source='applicant_profile.user.email')
    employer_email = serializers.EmailField(source='employer.email')

    class Meta:
        model = ReviewVacancy
        fields = [
            'id',
            'status',
            'vacancy',
            'employer_comment',
            'applicant_profile_email',  # Добавляем поле для адреса электронной почты профиля соискателя
            'employer_email',  # Добавляем поле для адреса электронной почты работодателя
        ]

    def create(self, validated_data):
        # Извлекаем почтовые адреса
        applicant_profile_email = validated_data.pop('applicant_profile').get('user').get('email')
        employer_email = validated_data.pop('employer').get('email')

        # Находим соответствующие объекты по почтовым адресам
        applicant_profile = Profile.objects.get(user__email=applicant_profile_email)
        employer = User.objects.get(email=employer_email)

        review_vacancy = ReviewVacancy.objects.create(
            applicant_profile=applicant_profile,
            employer=employer,
            **validated_data
        )

        return review_vacancy


class CompanyReviewSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email')

    class Meta:
        model = CompanyReview
        fields = ['id', 'company', 'user', 'rating', 'comment', 'created_date']

    def create(self, validated_data):
        user_email = validated_data.pop('user')
        user = User.objects.get(email=user_email)
        company_review= CompanyReview.objects.create(user=user, **validated_data)  # Используем **validated_data
        return company_review


