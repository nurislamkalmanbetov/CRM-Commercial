from datetime import date, datetime, timedelta

from applications.accounts.models import User
from django_filters import rest_framework as django_filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import filters, generics, status
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                     UpdateAPIView, mixins)
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Vacancy
from .serializers import *

class EmployerCompanyView(generics.CreateAPIView):
    serializer_class = EmployerCompanySerialzers
    queryset = EmployerCompany.objects.all()
    parser_classes = (MultiPartParser, FormParser)


    def perform_create(self, serializer):
        user_data = self.request.data.get('user')
        try:
            user = User.objects.get(email=user_data)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'User not found.'})

        if not user.is_employer:
            raise serializers.ValidationError({'detail': 'You are not an employer.'})

        if user.is_employer and not user.is_active:
            raise serializers.ValidationError({'detail': 'Your account is not active.'})
        
        serializer.save(user=user)


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class EmployerCompanyMixins(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin, GenericAPIView):
    
    queryset = EmployerCompany.objects.all()
    serializer_class = EmployerCompanySerialzers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__email']
    parser_classes = (MultiPartParser, FormParser)


    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({"message": "Успешно удалено"}, status=status.HTTP_200_OK)
        return response


class EmployerListApiView(ListAPIView):
    serializer_class = EmployerCompanySerialzers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__email']

    def get_queryset(self):
        return EmployerCompany.objects.all()



class CompanyReviewView(generics.CreateAPIView):
    serializer_class = CompanyReviewSerializer
    queryset = CompanyReview.objects.all()

    def perform_create(self, serializer):
        user_data = self.request.data.get('user')

        try:
            user = User.objects.get(email=user_data)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'Пользователь не найден.'})


        if not user.is_student:
            raise serializers.ValidationError({'detail': 'К сожалению только студенты могут оставлять отзывы.'})

       
        if not user.is_active:
            raise serializers.ValidationError({'detail': 'Ваш аккаунт не активен.'})
        
        serializer.save(user=user)


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class VacancyPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class VacancyListApiView(ListAPIView):
    serializer_class = VacancySerializers
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['employer_company__name', 'city','employer_company__user__email']
    search_fields = ['name', 'extra_info','employer_company__name']
    pagination_class = VacancyPagination  # Замените paginator на pagination_class

    def get_queryset(self):
        return Vacancy.objects.filter(is_vacancy_confirmed=True)


class VacancyListView(generics.CreateAPIView):
    serializer_class = VacancySerializers
    queryset = Vacancy.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        user_data = self.request.data.get('user')
        try:
            user = User.objects.get(email=user_data)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail': 'User not found.'})

        if not user.is_employer:
            raise serializers.ValidationError({'detail': 'You are not an employer.'})

        if user.is_employer and not user.is_active:
            raise serializers.ValidationError({'detail': 'Your account is not active.'})

        try:
            company = EmployerCompany.objects.get(user=user)
        except EmployerCompany.DoesNotExist:
            raise serializers.ValidationError({'detail': 'У вас не заполнен профиль. Заполните, пожалуйста, профиль.'})

        serializer.save(user=user)


    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class VacancyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')  # case-insensitive partial match for vacancy name
    city = django_filters.CharFilter(lookup_expr='exact')  # case-insensitive partial match for city
    salary = django_filters.CharFilter(lookup_expr='icontains')  # case-insensitive partial match for salary

    class Meta:
        model = Vacancy
        fields = ['name', 'city', 'salary']


class VacancyListCreateAPIView(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               generics.GenericAPIView):

    queryset = Vacancy.objects.all()
    serializer_class = VacancyFilterSerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = VacancyFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class VacancyChangeView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin, GenericAPIView):
    queryset = Vacancy.objects.filter(is_vacancy_confirmed=True)
    serializer_class = VacancyChangeSerializer
    parser_classes = (MultiPartParser, FormParser)


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({"message": "Успешно удалено"}, status=status.HTTP_200_OK)
        return response



class VacancyByEmployeeEmailAPIView(generics.ListAPIView):
    queryset = Vacancy.objects.filter(is_vacancy_confirmed=True)
    serializer_class = VacancySerializers
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['employer_company__user__email']
    search_fields = ['name', 'extra_info','employer_company__name']
    pagination_class = VacancyPagination




class ReviewVacancyCreateView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = ReviewVacancy.objects.filter(status='На рассмотрении')
    serializer_class = ReviewVacancySerializer

    def post(self, request, *args, **kwargs):
        vacancy_id = request.data.get('vacancy')
        
        if not vacancy_id:
            return Response({"error": "Вакансия не указана."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            return Response({"error": "Вакансия не найдена."}, status=status.HTTP_404_NOT_FOUND)
        
        if vacancy.required_positions_reviews >= vacancy.required_positions:
            return Response({"error": "Нельзя подать заявку на эту вакансию, так как все места уже заняты."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)


class ReviewVacancyListView(ListAPIView):
    queryset = ReviewVacancy.objects.all()
    serializer_class = ReviewVacancySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status','applicant_profile__user__email', 'employer__email']
    


INVITATION_COMMENT = "Ваша заявка была одобрена. Мы ждем вас!"
REJECTION_COMMENT = "К сожалению, ваша заявка была отклонена."


class ReviewVacancyUpdateView(UpdateAPIView):
    queryset = ReviewVacancy.objects.filter(status='На рассмотрении')
    serializer_class = ReviewVacancySerializer

    def update(self, request, *args, **kwargs):
        review_vacancy = self.get_object()
        
        # Получаем статус из запроса
        status_update = request.data.get("status", None)
        if not status_update:
            return Response({"error": "Необходимо указать статус."}, status=status.HTTP_400_BAD_REQUEST)

        if status_update == "Одобрено":
            review_vacancy.employer_comment = INVITATION_COMMENT
        elif status_update == "Отказано":
            review_vacancy.employer_comment = REJECTION_COMMENT
        else:
            return Response({"error": "Недействительный статус."}, status=status.HTTP_400_BAD_REQUEST)

        review_vacancy.status = status_update
        review_vacancy.save()

        serializer = self.get_serializer(review_vacancy)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NewVacancyView(ListAPIView):
    serializer_class = VacancySerializers
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    paginator = VacancyPagination()
    filterset_fields = ['employer_company', 'city']
    search_fields = ['name', 'extra_info']

    def get_queryset(self):
     
        current_date = datetime.now()
        
        three_days_ago = current_date - timedelta(days=3)

    
        return Vacancy.objects.filter(
            is_vacancy_confirmed=True,
            created_date__range=(three_days_ago, current_date)
        )



class ModeratedFeedbackListView(generics.ListAPIView):
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        return Feedback.objects.filter(status='moderated')


from django.http import JsonResponse
from .models import Event

from django.shortcuts import render

def events_calendar(request):
    return render(request, "admin/events_calendar.html")