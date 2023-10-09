from django.urls import path, include
from .views import *
from . import views

from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet)


urlpatterns = [
    path('signin/', UserLoginView.as_view(), name='signin'),
    path('profiles-create/', ProfileView.as_view(), name='profile-create'),
    path('user-lists/', UserView.as_view(), name='user-list'),
    path('user-list/<int:pk>/', UserListView.as_view({'patch': 'partial_update','put': 'update',})),
    # profiles
    path('profiles/', ProfileView.as_view(), name='profile'),
    path('profiles-list/', ProfileListView.as_view(), name='profile-list'),
    path('profiles-list-detail/<int:pk>/', ProfileListViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='profile-list-detail'),

    # Support
    path('support-request/', SupportRequestListCreateView.as_view(), name='support-request'),
    path('support-response/', SupportResponseCreateView.as_view(), name='support-response'),
    # Messages with Employer and Students
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageRetrieveUpdateDestroyView.as_view(), name='message-detail'),

    path('admin/create-user/', AdminCreateUserView.as_view(), name='admin-create-user'),

    # announcements - объявления
    path('api/', include(router.urls)),

    # forgot password
    path('a-password_reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('a-password_reset_confirm/<str:token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    path('export-pdf/<int:pk>/', generate_profile_pdf_view, name='export_pdf'),

]



