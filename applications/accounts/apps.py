from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'applications.accounts'

    def ready(self):
        from . import signals