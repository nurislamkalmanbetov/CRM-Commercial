from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import (exceptions, filters, generics, mixins, status,
                            viewsets)
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from .models import Profile, SupportRequest, SupportResponse
from .serializers import *
from django.template.loader import render_to_string
from random import randint


User = get_user_model()

class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.data['email']).first()
            if user is not None:
                return Response({"error": "Пользователь уже существует"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(
                email=serializer.data['email'],
                password=serializer.data['password']
            )
            
            verification_code = randint(1000, 9999)
            user.verification_code = verification_code
            user.save()
            context = {
                'verification_code': verification_code,
                
            }
          
            html_message = render_to_string('email_template.html', context)
            
          
            subject = 'Подтверждение регистрации'
            recipient_list = [user.email]  
            send_mail(subject, None, 'kalmanbetovnurislam19@gmail.com', recipient_list, html_message=html_message, fail_silently=False)
            print("ok")

            return Response({
                "messsage": "Успешная регистрация",
                "user": user.email,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyEmailAPIView(APIView):
    serializer_class = VerifyEmailSerializer
    queryset = User.objects.all()  

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            verification_code = serializer.data['verification_code']
            user = User.objects.filter(email=email).first()
            if user is None:
                return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
            if user.verification_code != verification_code:
                return Response({"error": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            user.is_verified_email = True
            user.verification_code = None
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "messsage": "Почта подтверждена",
                "user": user.email,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data['email'],password=serializer.validated_data['password'])
        except User.DoesNotExist:
            user = None
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Вход успешно выполнен',
                'email': user.email,
                'is_employer': user.is_employer,
                'is_student': user.is_student,

                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token)
                
            })
        else:
            return Response({'message': 'Неверный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)
        




class AdminCreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer  

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Отправка пароля на почту
            password = request.data.get('password')
            subject = 'Пароль для входа в систему'
            message = f'Ваш пароль: {password}'
            from_email = 'admin@example.com'  # Замените на адрес администратора

            recipient_list = [user.email]

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            except Exception as e:
                return Response({'message': 'Ошибка при отправке почты'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'Пользователь успешно создан и пароль отправлен на почту'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    


class ProfileView(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()  
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        user_data = self.request.data.get('user')
        try:
            user = User.objects.get(email=user_data)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'Вы не зарегистрированы'})
        
        if not user.is_student:
            raise serializers.ValidationError({'detail': 'Вы не студент'})
        
        serializer.save(user=user)

        # Устанавливаем поле is_active пользователя в значение True
        user.is_active = True
        user.save()
            
    def post(self, request, *args, **kwargs):
        
        return self.create(request, *args, **kwargs)

class ProfilePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

class ProfileListView(ListAPIView):
    serializer_class = ProfileListSerializer
    pagination_class = ProfilePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user__email', 'german', 'english', 'turkish', 'russian', 'chinese', 'university__name_ru', 'faculty__name_ru', 'driver_license', 'driving_experience']

    def get_queryset(self):
        return Profile.objects.select_related('user', 'university', 'faculty').all()


class ProfileListViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Profile.objects.select_related('user', 'university', 'faculty')
    serializer_class = ProfileListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user__email', 'german', 'english', 'turkish', 'russian', 'chinese', 'university__name_ru', 'faculty__name_ru', 'driver_license', 'driving_experience']



class UserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['email']

    

class SupportRequestListCreateView(generics.ListCreateAPIView):
    queryset = SupportRequest.objects.select_related('user').all()
    serializer_class = SupportRequestSerializer


  
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class SupportResponseCreateView(generics.CreateAPIView):
    queryset = SupportResponse.objects.all()
    serializer_class = SupportResponseSerializer

    def perform_create(self, serializer):
        serializer.save()
        response = serializer.instance
        user_email = response.support_request.user.email
        send_mail(
            'Ответ на ваш запрос на поддержку',
            response.message,
            'admin@example.com',  # ваш email
            [user_email],
            fail_silently=False,
        )

class PasswordResetRequestView(CreateAPIView):
    serializer_class = PasswordResetRequestSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = uuid.uuid4()
            user.password_reset_token = str(token)
            user.save()

            # Подготовка и отправка письма
            context = {
                'reset_link': f'http://127.0.0.1:8005/password_reset_confirm/{token}/',
                'token': token  # передаем токен в контекст для шаблона
            }
            html_content = render_to_string('password_reset_email.html', context)
            send_mail(
                'Сброс пароля',
                '',  # пустое тело для текстовой версии
                'from@example.com',
                [email],
                fail_silently=False,
                html_message=html_content
            )
        return Response({'detail': 'Если адрес электронной почты существует, ссылка для сброса пароля была отправлена.'})
    

class PasswordResetConfirmView(CreateAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def create(self, request, *args, **kwargs):
        token = kwargs.get('token')
        password = request.data.get('password')
        user = User.objects.filter(password_reset_token=token).first()
        if user:
            user.set_password(password)
            user.password_reset_token = None  # очистить токен после его использования
            user.save()
            return Response({'detail': 'Пароль успешно обновлен.'})
        return Response({'error': 'Неверный токен или он истек.'})

class ConnectionRequestListCreateView(generics.ListCreateAPIView):
    queryset = ConnectionRequest.objects.all()
    serializer_class = ConnectionRequestSerializer

    def post(self, request, *args, **kwargs):
        """Создание новой заявки на подключение"""
        return self.create(request, *args, **kwargs)

