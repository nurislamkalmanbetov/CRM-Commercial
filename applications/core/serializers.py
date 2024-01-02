from applications.accounts.models import User
from applications.accounts.models import Profile
from rest_framework import serializers
from applications.accounts.serializers import ProfileListSerializer
from .models import *
from django.contrib.auth import get_user_model
# from schedule.models import Event
<<<<<<< HEAD

=======
>>>>>>> origin/master



User = get_user_model()


# class EventSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
#     creator_email = serializers.EmailField(write_only=True)

#     class Meta:
#         model = Event
#         fields = ['id', 'title', 'start', 'end', 'description', 'creator', 'creator_email']
    
#     def validate_creator_email(self, value):
#         try:
#             user = User.objects.get(email=value)
#             return user
#         except User.DoesNotExist:
#             raise serializers.ValidationError("User with this email does not exist")

#     def create(self, validated_data):
#         creator_email = validated_data.pop('creator_email')
#         user = self.validate_creator_email(creator_email)
#         event = Event.objects.create(creator=user, **validated_data)
#         return event

#     def update(self, instance, validated_data):
#         creator_email = validated_data.pop('creator_email', None)
#         if creator_email:
#             user = self.validate_creator_email(creator_email)
#             instance.creator = user
=======
#     class Meta:
#         model = Event
#         fields = ['id', 'calendar','title', 'start', 'end', 'description', 'creator']

# class EventSerializer(serializers.ModelSerializer):
#     user_email = serializers.EmailField(write_only=True)

#     class Meta:
#         model = Event
#         fields = ['id', 'title', 'description', 'start_time', 'end_time', 'user_email']

#     def create(self, validated_data):
#         user_email = validated_data.pop('user_email')
#         user = User.objects.get(email=user_email)
#         event = Event.objects.create(user=user, **validated_data)
#         return event

#     def update(self, instance, validated_data):
#         user_email = validated_data.pop('user_email', None)
#         if user_email:
#             user = User.objects.get(email=user_email)
#             instance.user = user
>>>>>>> origin/master
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance

<<<<<<< HEAD
# class EventSerializer(serializers.ModelSerializer):
#     creator_email = serializers.EmailField(write_only=True)
#     calendar = serializers.PrimaryKeyRelatedField(queryset=Calendar.objects.all(), allow_null=True, required=False)

#     class Meta:
#         model = Event
#         fields = ['id', 'calendar', 'title', 'start', 'end', 'description', 'creator', 'creator_email']
    
#     def validate_creator_email(self, value):
#         try:
#             user = User.objects.get(email=value)
#             return user
#         except User.DoesNotExist:
#             raise serializers.ValidationError("User with this email does not exist")

#     def create(self, validated_data):
#         creator_email = validated_data.pop('creator_email')
#         user = self.validate_creator_email(creator_email)

#         calendar = validated_data.get('calendar')
#         if not calendar:
#             calendar = Calendar.objects.first()
#             if not calendar:
#                 raise serializers.ValidationError("No calendar available")

#         event = Event.objects.create(creator=user, calendar=calendar, **validated_data)
#         return event

#     def update(self, instance, validated_data):
#         creator_email = validated_data.pop('creator_email', None)
#         if creator_email:
#             user = self.validate_creator_email(creator_email)
#             instance.creator = user

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance

class EventSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'user_email']

    def create(self, validated_data):
        user_email = validated_data.pop('user_email')
        user = User.objects.get(email=user_email)
        event = Event.objects.create(user=user, **validated_data)
        return event

    def update(self, instance, validated_data):
        user_email = validated_data.pop('user_email', None)
        if user_email:
            user = User.objects.get(email=user_email)
            instance.user = user
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


=======
>>>>>>> origin/master
class InvitationSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True)
    vacancy_id = serializers.PrimaryKeyRelatedField(queryset=Vacancy.objects.all(), write_only=True)
    employer_email = serializers.EmailField(source='employer.user.email', write_only=True)
    employer_name = serializers.CharField(source='employer.name', read_only=True)
    vacancy_name = serializers.CharField(source='vacancy.name', read_only=True)
    
    class Meta:
        model = Invitation
        fields = ['id', 'user_email', 'message', 'status', 'vacancy_id', 'employer_email', 'employer_name', 'vacancy_name']

    def create(self, validated_data):
        user_email = validated_data.pop('user_email')
        employer_email = validated_data.pop('employer').get('user').get('email')
        employer = EmployerCompany.objects.get(user__email=employer_email)
        vacancy_id = validated_data.pop('vacancy_id').id

        try:
            user = User.objects.get(email=user_email, is_student=True, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("Student not found")

        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            raise serializers.ValidationError("Vacancy not found")

        status = validated_data.get('status')
        invitation = Invitation.objects.create(user=user, vacancy=vacancy, employer=employer, **validated_data)

        # Генерируем сообщение в зависимости от статуса
        if status == 'accepted':
            message = (f'Уважаемый(ая) {user.email}, '
                    f'мы внимательно изучили ваше резюме и были впечатлены вашими достижениями и опытом. '
                    f'С удовольствием приглашаем вас на собеседование в компанию {employer.name} '
                    f'на вакансию {vacancy.name}. Мы с нетерпением ожидаем встречи с вами и обсуждения деталей вашего возможного присоединения к нашей команде.')
        elif status == 'declined':
            message = (f'Уважаемый(ая) {user.email}, '
                    f'благодарим вас за проявленный интерес к вакансии {vacancy.name} в компании {employer.name}. '
                    f'После тщательного рассмотрения ряда кандидатур, к сожалению, мы приняли решение '
                    f'продолжить поиск. Это решение никак не отражает вашей квалификации, и мы надеемся на возможность сотрудничества в будущем. '
                    f'Желаем вам успехов и быстро найти подходящую позицию.')
        else:
            message = (f'Уважаемый(ая) {user.email}, '
                    f'рады сообщить вам, что вы были отобраны на рассмотрение для вакансии {vacancy.name} в компании {employer.name}. '
                    f'Пожалуйста, дайте нам знать о вашей готовности пройти собеседование и продолжить этот важный процесс.')

        invitation.message = message
        invitation.save()

        return invitation


class InvatationGetSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email')
    employer_email = serializers.EmailField(source='employer.user.email')
    
    class Meta:
        model = Invitation
        fields = ['id', 'user_email', 'message', 'status', 'vacancy', 'employer_email']


class EmployerCompanySerialzers(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email', required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = EmployerCompany
        fields = [
            'id',
            'user',
            # 'image_back',
            'icon',
            'name',
            'country',
            'description',
        ]

    def create(self, validated_data):
        user_email = validated_data.pop('user', None)  # Обратите внимание на изменение 'user.email' на 'user'
        user = User.objects.get(email=user_email)
        employercompany = EmployerCompany.objects.create(user=user, **validated_data)
        return employercompany

    def update(self, instance, validated_data):
        user_email = validated_data.pop('user', None)  # Извлекаем email, если он передан

        if user_email:  # Если email был передан, обновляем пользователя
            user = User.objects.get(email=user_email)
            instance.user = user

        # Обновление остальных полей
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()  # Сохраняем изменения
        return instance

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


class SubcategorySerializers(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category_name']

class CategorySerializers(serializers.ModelSerializer):
    subcategories = SubcategorySerializers(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']


class VacancySerializers(serializers.ModelSerializer):
    user = serializers.EmailField(source='employer_company.user.email')
    employer_company = serializers.CharField(source='employer_company.name')
    category = serializers.CharField(source='category.name', required=False)
    subcategory = serializers.CharField(source='subcategory.name', required=False)

    class Meta:
        model = Vacancy
        fields = [
            'id',
            'user',
            'employer_company',
            'picture',
            'employer_company',
            'name', 
            'category',
            'subcategory',
            'salary', 
            'exchange',
            'duty', 
            'city', 
            'language',
            'proficiency',
            'accomodation_type', 
            'accomodation_cost', 
            'is_vacancy_confirmed', 
            'insurance',
            'required_positions',
            'transport', 
            'contact_info', 
            'destination_point', 
            'employer_dementions', 
            'extra_info',
        ]

    def create(self, validated_data):
        user_email = validated_data.pop('employer_company').get('user').get('email')
        user = EmployerCompany.objects.get(user__email=user_email)

        category_data = validated_data.pop('category', None)
        subcategory_data = validated_data.pop('subcategory', None)

        category_instance = None
        if category_data:
            category_instance, created = Category.objects.get_or_create(**category_data)

        subcategory_instance = None
        if subcategory_data:
            subcategory_data['category'] = category_instance
            subcategory_instance, created = Subcategory.objects.get_or_create(**subcategory_data)

        # Check if subcategory_instance is a dictionary (indicating an error)
        if isinstance(subcategory_instance, dict):
            raise serializers.ValidationError({'subcategory': ['Invalid subcategory data']})

        # Create the Vacancy object after obtaining the necessary category_instance
        vacancy = Vacancy.objects.create(employer_company=user, category=category_instance, subcategory=subcategory_instance, **validated_data)
        return vacancy
    

    def update(self, validated_data):
        user_email = validated_data.pop('employer_company').get('user').get('email')
        user = User.objects.get(email=user_email)
        vacancy = Vacancy.objects.update(employer_company=user.employer_company, **validated_data)
        return vacancy

class VacancyFilterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancyChangeSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='employer_company.user.email', read_only=True)
    category_name = serializers.SerializerMethodField()
    subcategory_name = serializers.SerializerMethodField()
    employer_company_name = serializers.SerializerMethodField()

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    def get_subcategory_name(self, obj):
        return obj.subcategory.name if obj.subcategory else None

    def get_employer_company_name(self, obj):
        return obj.employer_company.name if obj.employer_company else None

    class Meta:
        model = Vacancy
        fields = [
            'id', 'picture', 'user', 'name', 'category_name',
            'subcategory_name', 'salary', 'exchange', 'city', 'accomodation_cost', 'insurance',
            'transport', 'contact_info', 'destination_point', 'employer_dementions', 'extra_info', 'duty',
            'language', 'required_positions', 'proficiency', 'accomodation_type', 'employer_company_name'
        ]



class ReviewVacancySerializer(serializers.ModelSerializer):
    applicant_profile_email = serializers.EmailField(source='applicant_profile.user.email')
    employer_email = serializers.EmailField(source='employer.email')
    applicant_profile_data = ProfileListSerializer(source='applicant_profile', read_only=True)
    vacancy_name = serializers.CharField(source='vacancy.name', read_only=True )

    

    class Meta:
        model = ReviewVacancy
        fields = [
            'id',
            'status',
            'vacancy',
            'vacancy_name',
            'employer_comment',
            'applicant_profile_email',
            'applicant_profile_data',  # Добавляем поле для адреса электронной почты профиля соискателя
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


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'text', 'user', 'created_at', 'status')

class ImprovementIdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprovementIdea
        fields = ('id', 'text', 'user', 'created_at', 'status')