from django.apps import AppConfig


class EducationConfig(AppConfig):
    name = 'applications.core'

    def ready(self):
       from . import signals