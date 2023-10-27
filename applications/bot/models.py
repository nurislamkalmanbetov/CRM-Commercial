from django.db import models

class TelegramUser(models.Model):
    user_id = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.username

