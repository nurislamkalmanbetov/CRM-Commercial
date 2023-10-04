from django.urls import path, include
from .views import *
from . import views


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


    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]



