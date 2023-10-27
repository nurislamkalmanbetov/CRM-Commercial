from django.urls import path
from . import views

urlpatterns = [
    path('create_telegram_user/', views.create_telegram_user, name='create_telegram_user'),
]



