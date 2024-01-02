from django.urls import include, path

from .views import *

urlpatterns = [
    path('signup/', RegistrationAPIView.as_view(), name='signup'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('custom-token/', CustomTokenObtainPairView.as_view(), name='custom-token-obtain'),

    path('signin/', UserLoginView.as_view(), name='signin'),
    # Profile
    path('profiles/', ProfileView.as_view(), name='profile'),
    path('profiles-list/', ProfileListView.as_view(), name='profile-list'),
    path('profiles-list-detail/<int:pk>/', ProfileListViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='profile-list-detail'),
    # User
    path('user-lists/', UserView.as_view(), name='user-list'),
    #requests
    # path('support-request/', SupportRequestListCreateView.as_view(), name='support-request'),
    # path('support-response/', SupportResponseCreateView.as_view(), name='support-response'),
    #Admin create user
    # path('admin/create-user/', AdminCreateUserView.as_view(), name='admin-create-user'),
    # path('a-password_reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    # path('a-password_reset_confirm/<str:token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    # path('connection-requests/', ConnectionRequestListCreateView.as_view(), name='connection-requests-list-create'),
]



