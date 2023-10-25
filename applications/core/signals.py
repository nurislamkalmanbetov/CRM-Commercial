from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vacancy
from django.conf import settings
from django.core.mail import send_mail
from .models import ReviewVacancy




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
            f'Язык: {instance.language}\n'
            f'Компания: {instance.employer_company}\n'
            f'Требуемые должности: {instance.required_positions}\n'
            f'Отзывы о требуемых должностях: {instance.required_positions_reviews}\n'
            f'Обязанности: {instance.duty}\n'
            f'Стоимость проживания: {instance.accomodation_cost}\n'
            f'Страховка: {instance.insurance}\n'
            f'Размер компании: {instance.employer_dementions}\n'
            f'Дополнительная информация: {instance.extra_info}\n'
            f'Дата создания: {instance.created_date}\n'
        )

        from_email = settings.EMAIL_HOST_USER

        # Получаем список всех активных студентов
        users = User.objects.filter(is_active=True, is_student=True)

        # Отправляем уведомление каждому активному студенту
        for user in users:
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])



@receiver(post_save, sender=ReviewVacancy)
def send_email_notification(sender, instance, created, **kwargs):
    if created:
        return

    subject = 'Статус вашего отклика на вакансию обновлен'
    
    if instance.employer_comment:
        comment = f"\n\nКомментарий от работодателя: {instance.employer_comment}"
    else:
        comment = ""

    message = f'Отклик на вакансию "{instance.vacancy.name}" обновлен до статуса "{instance.status}".' + comment
    recipient_list = [instance.applicant_profile.user.email]  # Email соискателя

    send_mail(subject, message, recipient_list)


