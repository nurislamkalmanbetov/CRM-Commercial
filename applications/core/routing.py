from django.urls import re_path

from core.consumers import VacancyConsumer

websocket_urlpatterns = [
    re_path(r'ws/vacancies/$', VacancyConsumer.as_asgi()),
]