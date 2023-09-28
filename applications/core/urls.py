from django.urls import path
from .views import *


urlpatterns = [
    path('employer-company-create/', EmployerCompanyView.as_view(), name='employer-company'),
    #Vacancy
    path('vacancy/', VacancyListView.as_view(), name='vacancy'),
    path('vacancy-change-detail/<int:pk>/', VacancyChangeView.as_view(), name='vacancy-change-detail'),
    path('individual-vacancies/', VacancyByEmployeeEmailAPIView.as_view(), name='individual-vacancies'),
    path('new-vacancy/', NewVacancyView.as_view(), name='new-vacancy'),
    path('vacancies-filter/', VacancyListCreateAPIView.as_view(), name='vacancies-filter'),
    path('vacancies-list/', VacancyListApiView.as_view(), name='vacancies-list'),
    #Review
    
    path('review-create', ReviewVacancyCreateView.as_view(), name='review-create'),
    path('review-get', ReviewVacancyListView.as_view(), name='review-get'),
    path('review-patch/<int:pk>/', ReviewVacancyUpdateView.as_view(), name='review-patch'),

    path('feedback-get', ModeratedFeedbackListView.as_view(), name='feedback-get'),

    # path('university/', UniversityView.as_view(), name='university'),
    # path('faculty/', FacultyView.as_view(), name='faculty'),
]
