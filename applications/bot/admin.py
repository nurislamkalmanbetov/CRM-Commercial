from django.contrib import admin

# Register your models here.
from .models import TelegramUser

class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'is_manager')
    list_filter = ('is_manager',)
    search_fields = ('user_id', 'username')

admin.site.register(TelegramUser, TelegramUserAdmin)


