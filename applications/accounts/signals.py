import requests
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, SupportResponse, Payment, Announcement, ConnectionRequest
from django.core.mail import send_mail
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# from applications.bot.models import TelegramUser

# @receiver(post_save, sender=User)
# def send_password_email(sender, instance, created, **kwargs):
#     if created:
#         subject = 'Данные для входа в систему'
#         message = f'Добро пожаловать!\n\n'
#         message += f'Логин (Gmail): {instance.email}\n'
#         message += f'Пароль: {instance.password}\n'
#         message += f'можете перейти на наш сайт https://www.iwex.kg/ \n'
        
#         if instance.phone:
#             message += f'Номер телефона: {instance.phone}\n'
        
#         if instance.whatsapp_phone:
#             message += f'Номер Whatsapp: {instance.whatsapp_phone}\n'
        
#         from_email = 'kalmanbetovnurislam19@gmail.com'  

#         recipient_list = [instance.email]

#         try:
#             send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#         except Exception as e:
#             pass


@receiver(post_save, sender=ConnectionRequest)
def send_connection_request(sender, instance, created, **kwargs):
        message = f'Есть новая заявка на регистрацию!\n\n'
        message += f'ФИО: {instance.full_name}\n'
        message += f'Почта: {instance.email}\n' 
        if instance.phone:
            message += f'Номер телефона: {instance.phone}\n'
        message += f'ID: {instance.id}\n\n'
        message += f'Дата заявки: {instance.request_date}'
        link = f'https://crm.iwex.kg/admin/accounts/connectionrequest/{instance.id}/change/'
        bot_url = 'https://api.telegram.org/bot6597777546:AAGh8VSz_m2FYkNqeudw27Qp26mKAr4hT94/sendMessage'

        inline_keyboard = {
            "inline_keyboard": [[{"text": "Перейти", "url": link}]]
        }

        data = {
            'chat_id': 6673864170,
            'text': message,
            'reply_markup': json.dumps(inline_keyboard)
        }

        response = requests.post(bot_url, data=data)

        if response.status_code == 200:
            print('ok')


@receiver(post_save, sender=SupportResponse)
def send_response_email(sender, instance, created, **kwargs):
    if created:
        user_email = instance.support_request.user.email
        send_mail(
            'Ответ на ваш запрос на поддержку',
            instance.message,
            'admin@example.com',
            [user_email],
            fail_silently=False,
        )

@receiver(user_logged_in)
def set_start_of_work(sender, request, user, **kwargs):
    if user.is_staff:
        user.start_of_work = timezone.now()
        user.save()

@receiver(user_logged_out)
def set_end_of_work(sender, request, user, **kwargs):
    if user.is_staff:
        user.end_of_work = timezone.now()
        user.save()

@receiver(post_save, sender=Payment)
def send_payment_notification(sender, instance, created, **kwargs):
    subject = 'Уведомление об оплате'
    message = f'Информация об оплате:\n'
    message += f'Оплачено: {instance.amount_paid}\n'
    message += f'Остаток: {instance.remaining_amount}\n'
    message += f'Оплачено полностью: {"Да" if instance.is_fully_paid else "Нет"}\n'
    message += f'Дата оплаты: {instance.payment_date.strftime("%d.%m.%Y")}\n'
    if instance.due_date:
        message += f'Крайний срок оплаты: {instance.due_date.strftime("%d.%m.%Y")}\n'
    else:
        message += f'Крайний срок оплаты: не указан\n'

    from_email = 'your_email@gmail.com'  
    recipient_list = [instance.user.email]  # Электронная почта пользователя, который произвел оплату

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        # Здесь вы можете добавить логирование ошибок или другие действия
        pass 


@receiver(post_save, sender=Announcement)
def send_announcement_email(sender, instance, **kwargs):
    recipients = []

    if instance.specific_student:
        if instance.specific_student.is_student and instance.specific_student.is_active:
            recipients.append(instance.specific_student)
        else:
            print(f"Студент {instance.specific_student} не активен и не получит объявление.")
    elif instance.send_to_students:
        recipients.extend(User.objects.filter(is_student=True, is_active=True))

    if instance.specific_employer:
        if instance.specific_employer.is_employer and instance.specific_employer.is_active:
            recipients.append(instance.specific_employer)
        else:
            print(f"Работодатель {instance.specific_employer} не активен и не получит объявление.")
    elif instance.send_to_employers:
        recipients.extend(User.objects.filter(is_employer=True, is_active=True))

    if recipients:
        subject = f"Новое объявление: {instance.title}"
        message = f"Новое объявление:\n\n{instance.title}\n\n{instance.content}"
        from_email = settings.DEFAULT_FROM_EMAIL

        text_content = strip_tags(message)

        for recipient in recipients:
            html_content = render_to_string('layouts/announcement_email_template.html', {
                'title': instance.title,
                'content': instance.content,
                'photo_url': instance.photo.url if instance.photo else None,
                'video_url': instance.video.url if instance.video else None,
            })

            email = EmailMultiAlternatives(subject, text_content, from_email, [recipient.email])
            email.attach_alternative(html_content, "text/html")
            if instance.photo:
                email.attach_file(instance.photo.path)
            if instance.video:
                email.attach_file(instance.video.path)

            email.send()
