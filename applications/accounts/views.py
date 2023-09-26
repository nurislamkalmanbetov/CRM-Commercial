from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import exceptions, filters, generics, status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
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
            user = User.objects.get(email=serializer.validated_data['email'],password=serializer.validated_data['password'])
        except User.DoesNotExist:
            user = None
        if user is not None:
            refresh = RefreshToken.for_user(user)
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

class ProfilePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

class ProfileListView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    pagination_class = ProfilePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user__email', 'german', 'english', 'turkish', 'russian', 'chinese','university__name_ru','faculty__name_ru', 'driver_license', 'driving_experience',]
    

class UserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['email']

    
class UserListView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListPutchSerializer
    parser_classes = (MultiPartParser, FormParser)
