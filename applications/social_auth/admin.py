from django.contrib import admin
from applications.accounts.models import User

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User)
