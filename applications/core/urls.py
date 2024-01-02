from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'events', EventViewSet)

# router = DefaultRouter()
# router.register(r'events', EventViewSet)

urlpatterns = [
<<<<<<< HEAD
    path('calendar/', include(router.urls)),
=======
    # path('calendar/', include(router.urls)),
>>>>>>> origin/master
    path('employer-company-create/', EmployerCompanyView.as_view(), name='employer-company'),
    path('employer-company-list/', EmployerListApiView.as_view(), name='employer-company-list'),
    path('employer-company-change-detail/<int:pk>/', EmployerCompanyMixins.as_view(), name='employer-company-change-detail'),

    #Vacancy
    path('vacancy/', VacancyListView.as_view(), name='vacancy'),
    path('vacancy-change-detail/<int:pk>/', VacancyChangeView.as_view(), name='vacancy-change-detail'),
    path('individual-vacancies/', VacancyByEmployeeEmailAPIView.as_view(), name='individual-vacancies'),
    path('new-vacancy/', NewVacancyView.as_view(), name='new-vacancy'),
    path('vacancies-filter/', VacancyListCreateAPIView.as_view(), name='vacancies-filter'),
    path('vacancies-list/', VacancyListApiView.as_view(), name='vacancies-list'),
    
    # category
    path('categories/', CategoryView.as_view(), name='category-list'), 

    #Review
    path('company-review-create/', CompanyReviewView.as_view(), name='company-review'),
    path('review-create', ReviewVacancyCreateView.as_view(), name='review-create'),
    path('review-get', ReviewVacancyListView.as_view(), name='review-get'),
    path('review-patch/<int:pk>/', ReviewVacancyUpdateView.as_view(), name='review-patch'),
    
    # invation
    path('invitations/create/', InvitationCreateView.as_view(), name='invitation-create'),
    path('invitations/', InvitationListView.as_view(), name='invitation-list'),
    path('invitations/<int:pk>/', InvitationUpdateView.as_view(), name='invitation-update'),
 
    path('feedback-get', ModeratedFeedbackListView.as_view(), name='feedback-get'),

    # path('university/', UniversityView.as_view(), name='university'),
    # path('faculty/', FacultyView.as_view(), name='faculty'),
]
