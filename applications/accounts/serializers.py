from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .serializers import *
from .models import *

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


from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email')
    university = serializers.CharField(source='university.name_ru')
    faculty = serializers.CharField(source='faculty.name_ru')

    class Meta:
        model = Profile
        fields = ('id', 'user', 'photo', 'first_name', 'last_name', 'telephone',
        'bday', 'gender','been_to_germany', 'nationality', 'birth_country','reg_apartment',
        'university','faculty','study_start','study_end','direction',
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
        'university','faculty','study_start','study_end','direction',
        'german', 'english', 'turkish', 'russian', 'chinese', 
        'driver_license', 'driving_experience', 'cat_a', 'cat_b', 'cat_c', 'cat_d', 'cat_e', 'tractor', 'transmission', 
        'reading', 'singing', 'travelling', 'yoga', 'dancing', 'sport', 'drawing', 'computer_games', 'guitar', 'films', 'music', 'knitting', 'cooking', 'fishing', 'photographing', 
        )


class ProfileHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileHistory
        fields = '__all__'   


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'avatar', 'email', 'phone', 'whatsapp_phone', 'is_employer', 'is_active')


class UserListPutchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'avatar')


class SupportRequestSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email')

    class Meta:
        model = SupportRequest
        fields = [
            'id', 
            'user', 
            'message', 
            'created_at',
        ]

    def create(self, validated_data):
        user_email = validated_data.pop('user').get('email')
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user": "User with this email does not exist."})
        supportrequest = SupportRequest.objects.create(user=user, **validated_data)
        return supportrequest


class SupportResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportResponse
        fields = ['id', 'support_request', 'message', 'created_at', 'sent']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.EmailField()
    recipient = serializers.EmailField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp']

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email, is_active=True)
            if not (user.is_student or user.is_employer):
                raise serializers.ValidationError("Email не соответствует студенту или работодателю.")
            return email
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователя с таким email не существует.")

    def validate_sender(self, email):
        return self.validate_email(email)

    def validate_recipient(self, email):
        return self.validate_email(email)

    def create(self, validated_data):
        sender_email = validated_data.pop('sender')
        recipient_email = validated_data.pop('recipient')

        sender = User.objects.get(email=sender_email)
        recipient = User.objects.get(email=recipient_email)

        message = Message.objects.create(sender=sender, recipient=recipient, **validated_data)
        return message


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'


class UserConnectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone', 'is_employer', 'is_student')


class ConnectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionRequest
        fields = ('id', 'full_name', 'email', 'phone', 'request_date', 'manager_notes', 'call_date', 'called', 'consulted', 'call_later')



from rest_framework import serializers
from .models import RefreshToken

class InvalidateRefreshTokensSerializer(serializers.Serializer):
    client_id = serializers.CharField(required=True)

    def create(self, validated_data):
        client_id = validated_data.get('client_id')

        # Инвалидация токенов для переданного client_id
        try:
            # Получаем все токены для указанного client_id
            tokens = RefreshToken.objects.filter(client_id=client_id)

            # Инвалидируем найденные токены
            for token in tokens:
                token.is_valid = False
                token.save()

            return validated_data  # Подтверждение успешной инвалидации
        except Exception as e:
            # Обработка ошибки, если что-то пошло не так
            raise serializers.ValidationError("Failed to invalidate tokens")


