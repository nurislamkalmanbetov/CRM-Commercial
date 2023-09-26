from .models import Vacancy
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save



from django.contrib.auth import get_user_model
User = get_user_model()

@receiver(post_save, sender=Vacancy)
def send_vacancy_notification(sender, instance, created, **kwargs):
    if created:
        User = get_user_model()  # Получаем модель User с использованием get_user_model

        subject = 'Новая вакансия доступна!'
        message = f'Новая вакансия: {instance.name}\nЗарплата: {instance.salary}\nГород: {instance.city}'
        from_email = settings.EMAIL_HOST_USER

        # Получаем список всех активных студентов
        users = User.objects.filter(is_active=True, is_student=True)

        # Отправляем уведомление каждому активному студенту
        for user in users:
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])