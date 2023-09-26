from django.urls import path, include
from .views import *


urlpatterns = [
    path('signin/', UserLoginView.as_view(), name='signin'),
    path('profiles/', ProfileView.as_view(), name='profile'),
    path('profiles-list/', ProfileListView.as_view(), name='profile-list'),
    path('user-lists/', UserView.as_view(), name='user-list'),
    path('user-list/<int:pk>/', UserListView.as_view({'patch': 'partial_update','put': 'update',})),
    # .
]



