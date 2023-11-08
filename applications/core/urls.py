from django.urls import path
from .views import *



urlpatterns = [
    path('vacancy/', VacancyListView.as_view(), name='vacancy'),
    path('vacancy-change-detail/<int:pk>/', VacancyChangeView.as_view(), name='vacancy-change-detail'),
    path('individual-vacancies/', VacancyByEmployeeEmailAPIView.as_view(), name='individual-vacancies'),
    # path('favorite-vacancies/', FavoriteVacancyCreateAPIView.as_view(), name='favorite-vacancy'),
    path('vacancies-filter/', VacancyListCreateAPIView.as_view(), name='vacancies-filter'),
    path('review-get', ReviewVacancyListView.as_view(), name='review-get'),
    path('new-vacancy/', NewVacancyView.as_view(), name='new-vacancy'),
    path('review-create', ReviewVacancyCreateView.as_view(), name='review-create'),
    path('review-patch/<int:pk>/', ReviewVacancyUpdateView.as_view(), name='review-patch'),
    path('company-review-create/', CompanyReviewView.as_view(), name='company-review'),
                                
    # invation
    path('invitations/create/', InvitationCreateView.as_view(), name='invitation-create'),
    path('invitations/', InvitationListView.as_view(), name='invitation-list'),
    path('invitations/<int:pk>/', InvitationUpdateView.as_view(), name='invitation-update'),
    
    # employer
    path('employer-company-create/', EmployerCompanyView.as_view(), name='employer-company'),
    path('employer-company-list/', EmployerListApiView.as_view(), name='employer-company-list'),
    path('employer-company-change-detail/<int:pk>/', EmployerCompanyMixins.as_view(), name='employer-company-change-detail'),
    # path('university/', UniversityView.as_view(), name='university'),
    # path('faculty/', FacultyView.as_view(), name='faculty'),



    path('employer_company/<int:company_id>/', employer_company_detail, name='employer_company_detail'),
]





