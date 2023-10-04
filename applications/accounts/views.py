from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import (exceptions, filters, generics, mixins, permissions,
                            status, viewsets)
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, ListAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Profile
from .serializers import *
from .serializers import UserLoginSerializer

User = get_user_model()




class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        except User.DoesNotExist:
            user = None
        if user is not None:
            refresh = RefreshToken.for_user(user)

            # Отправка пароля на почту, если пользователь активен и студент
            if user.is_student and user.is_active:
                subject = 'Пароль для входа в систему'
                message = f'Ваш пароль: {serializer.validated_data["password"]}'
                from_email = 'noreply@example.com'  # Замените на ваш адрес электронной почты

                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return Response({
                'message': 'Вход успешно выполнен',
                'email': user.email,
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token)
            })
        else:
            return Response({'message': 'Неверный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProfileView(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()  # предположим, что модель называется Profile
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        user_data = self.request.data.get('user')
        try:
            user = User.objects.get(email=user_data)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'Вы не зарегистрированы'})
        
        if not user.is_student:
            raise serializers.ValidationError({'detail': 'Вы не студент'})
            
        if user.is_student and not user.is_active:
            raise serializers.ValidationError({'detail': 'Ваш профиль не активный'})
        
        serializer.save(user=user)
            
    def post(self, request, *args, **kwargs):
        
        return self.create(request, *args, **kwargs)


class ProfileListView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user__email', 'german', 'english', 'turkish', 'russian', 'chinese','university__name_ru','faculty__name_ru', 'driver_license', 'driving_experience',]


class ProfileListViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user__email', 'german', 'english', 'turkish', 'russian', 'chinese','university__name_ru','faculty__name_ru', 'driver_license', 'driving_experience',]


class SupportRequestListCreateView(generics.ListCreateAPIView):
    queryset = SupportRequest.objects.all()
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


class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


class AdminCreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer  #  сериализатор пользователя

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Отправка пароля на почту
            password = request.data.get('password')
            subject = 'Пароль для входа в систему'
            message = f'Ваш пароль: {password}'
            from_email = 'admin@example.com'  # адрес администратора

            recipient_list = [user.email]

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            except Exception as e:
                return Response({'message': 'Ошибка при отправке почты'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'Пользователь успешно создан и пароль отправлен на почту'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileHistoryView(APIView):

    serializer_class = ProfileHistorySerializer

    def get(self, request):
        profile_histories = ProfileHistory.objects.all()
        serializer = self.serializer_class(profile_histories, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProfileHistorySerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['email']


class UserListView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListPutchSerializer
    parser_classes = (MultiPartParser, FormParser)


from django.shortcuts import render

def admin_dashboard(request):
    # Здесь можно добавить какую-либо логику, если нужно
    return render(request, 'admin_dashboard.html')

