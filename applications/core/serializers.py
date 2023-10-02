from rest_framework import serializers
from .models import *
from applications.accounts.models import User

class EmployerCompanySerialzers(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email')

    class Meta:
        model = EmployerCompany
        fields = [
            'id',
            'icon',
            'user',
            'name',
            'country',
            'description',
        ]

    def create(self, validated_data):
        user_email = validated_data.pop('user')
        user = User.objects.get(email=user_email)
        employercompany = EmployerCompany.objects.create(user=user, **validated_data)  # Используем **validated_data
        return employercompany

class VacancySerializers(serializers.ModelSerializer):
    # employer_company = EmployerCompanySerialzers(read_only=True)
    user = serializers.EmailField(source='employer_company.user.email')


    class Meta:
        model = Vacancy
        fields = [
            'id',
            'user',
            'picture',
            'name', 
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
        vacancy = Vacancy.objects.create(employer_company=user, **validated_data)
        return vacancy
    

    def update(self, validated_data):
        user_email = validated_data.pop('employer_company').get('user').get('email')
        user = User.objects.get(email=user_email)
        vacancy = Vacancy.objects.update(employer_company=user.employer_company, **validated_data)
        return vacancy

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
    

class VacancyFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancyChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['id', 'picture', 'name', 'salary', 'city', 'accomodation_cost', 'insurance', 'transport',
                  'contact_info', 'destination_point', 'employer_dementions', 'extra_info', 'duty', 'language','required_positions',
                  'proficiency', 'accomodation_type',
        ]



class ReviewVacancySerializer(serializers.ModelSerializer):
    profile_review = serializers.EmailField(source='profile_review.user.email')
    vacancy_review = serializers.EmailField(source='vacancy_review.user.email')

    class Meta:
        model = ReviewVacancy
        fields = ['profile_review', 'vacancy_review']

    def create(self, validated_data):
        # Добавьте логику создания отклика на вакансию
        return ReviewVacancy.objects.create(**validated_data)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'text', 'user', 'created_at', 'status')

class ImprovementIdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprovementIdea
        fields = ('id', 'text', 'user', 'created_at', 'status')