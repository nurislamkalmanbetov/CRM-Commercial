from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vacancy
from applications.accounts.models import SupportResponse
from django.conf import settings
from django.core.mail import send_mail


from django.contrib.auth import get_user_model
User = get_user_model()

@receiver(post_save, sender=Vacancy)
def send_vacancy_notification(sender, instance, created, **kwargs):
    if created:
        User = get_user_model()  # Получаем модель User с использованием get_user_model

        subject = 'Новая вакансия доступна!'
        message = (
            f'Новая вакансия: {instance.name}\n'
            f'Зарплата: {instance.salary}\n'
            f'Город: {instance.city}\n'
            f'Дата создания: {instance.created_date}\n'
        )

        from_email = settings.EMAIL_HOST_USER

        # Получаем список всех активных студентов
        users = User.objects.filter(is_active=True, is_student=True)

        # Отправляем уведомление каждому активному студенту
        for user in users:
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])


@receiver(post_save, sender=SupportResponse)
def send_response_email(sender, instance, created, **kwargs):
    if created:  # Проверка, что ответ был только что создан
        user_email = instance.support_request.user.email
        send_mail(
            'Ответ на ваш запрос на поддержку',
            instance.message,
            'admin@example.com',
            [user_email],
            fail_silently=False,
        )


@receiver(post_save, sender=User)
def send_password_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Данные для входа в систему'
        message = f'Добро пожаловать!\n\n'
        message += f'Логин (Gmail): {instance.email}\n'
        message += f'Пароль: {instance.password}\n'
        message += f'можете перейти на наш сайт https://www.iwex.kg/ \n'
        
        if instance.phone:
            message += f'Номер телефона: {instance.phone}\n'
        
        if instance.whatsapp_phone:
            message += f'Номер Whatsapp: {instance.whatsapp_phone}\n'
        
        from_email = 'kalmanbetovnurislam19@gmail.com'  

        recipient_list = [instance.email]

        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except Exception as e:
            pass
