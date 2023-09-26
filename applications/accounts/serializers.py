from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *
from .serializers import *

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(

            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email')
    university = serializers.CharField(source='university.name_ru')
    faculty = serializers.CharField(source='faculty.name_ru')

    class Meta:
        model = Profile
        fields = ('id', 'user', 'photo', 'first_name', 'last_name', 'telephone',
        'bday', 'gender','been_to_germany', 'nationality', 'birth_country','reg_apartment',
        'university','faculty','study_start','study_end',
        'german', 'english', 'turkish', 'russian', 'chinese', 
        'driver_license', 'driving_experience', 'cat_a', 'cat_b', 'cat_c', 'cat_d', 'cat_e', 'tractor', 'transmission', 
        'reading', 'singing', 'travelling', 'yoga', 'dancing', 'sport', 'drawing', 'computer_games', 'guitar', 'films', 'music', 'knitting', 'cooking', 'fishing', 'photographing', 
        )

    def create(self, validated_data):
        user_email = validated_data.pop('user')
        user = User.objects.get(email=user_email)

        university_name = validated_data.pop('university').get('name_ru')
        university = University.objects.get(name_ru=university_name)

        faculty_name = validated_data.pop('faculty').get('name_ru')
        faculty = Faculty.objects.get(name_ru=faculty_name)
        
        profile = Profile.objects.create(
            user=user,
            university=university,
            faculty=faculty,
            **validated_data
        )
        return profile

class ProfileListSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email', read_only=True)
    university = serializers.CharField(source='university.name_ru', read_only=True)
    faculty = serializers.CharField(source='faculty.name_ru', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'photo', 'first_name', 'last_name', 'telephone',
        'bday', 'gender','been_to_germany', 'nationality', 'birth_country','reg_apartment',
        'university','faculty','study_start','study_end',
        'german', 'english', 'turkish', 'russian', 'chinese', 
        'driver_license', 'driving_experience', 'cat_a', 'cat_b', 'cat_c', 'cat_d', 'cat_e', 'tractor', 'transmission', 
        'reading', 'singing', 'travelling', 'yoga', 'dancing', 'sport', 'drawing', 'computer_games', 'guitar', 'films', 'music', 'knitting', 'cooking', 'fishing', 'photographing', 
        )

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'avatar', 'email', 'phone', 'whatsapp_phone', 'is_employer', 'is_active')


class UserListPutchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'avatar')
