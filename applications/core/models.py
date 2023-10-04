from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import Sum

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta



# from django.contrib.auth import get_user_model
# User = get_user_model()

class University(models.Model):
    name = models.CharField('Название', max_length=500)
    name_ru = models.CharField('Название на русском', max_length=500)
    name_de = models.CharField('Название на немецком', max_length=500)
    address = models.TextField('Адрес на немецком')
    phone = models.CharField('Номер телефона', max_length=50)
    site = models.URLField('Сайт университета')

    class Meta:
        ordering = ['name_ru', ]
        verbose_name = 'университет'
        verbose_name_plural = 'университеты'

    def __str__(self):
        return self.name_ru


class Faculty(models.Model):
    name_ru = models.CharField('Название на русском', max_length=500)
    name_de = models.CharField('Название на немецком', max_length=500)

    class Meta:
        ordering = ['name_ru', ]
        verbose_name = 'факультет'
        verbose_name_plural = 'факультеты'

    def __str__(self):
        return self.name_ru


class Notification(models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.SET_NULL, verbose_name='Пользователь',
                                related_name='notifications', blank=True, null=True)
    author = models.CharField('Автор', default='iWEX', max_length=500)
    title = models.CharField('Заголовок', default='Сообщение', max_length=500)
    message = models.CharField('Сообщение', max_length=1000)
    date = models.DateTimeField('Время отправки', auto_now_add=True)
    is_viewed = models.BooleanField('Просмотрено', default=False)

    class Meta:
        ordering = ['-date', ]
        verbose_name = 'уведомление'
        verbose_name_plural = 'уведомления'

    def __str__(self):
        return self.title


class ContractAdmin(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    )

    first_name = models.CharField('Имя', max_length=500, default='')
    last_name = models.CharField('Фамилия', max_length=500, default='')
    father_name = models.CharField('Отчество', max_length=500, default='', blank=True)
    gender = models.CharField('Пол', choices=GENDER_CHOICES, max_length=1, default=MALE)
    patent_id = models.CharField('Номер патента (N1234567)', max_length=20, default='')
    patent_date = models.DateField('Дата получения патента')
    given_by = models.TextField('Выдан (УГНС по Ленинскому району)')

    class Meta:
        ordering = ['id', ]
        verbose_name = 'администратор для контрактов'
        verbose_name_plural = 'администраторы для контрактов'

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        full_name = f'{self.last_name} {self.first_name}'
        full_name = f'{full_name} {self.father_name}' if self.father_name else full_name
        return full_name


class EmployerCompany(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name='Работодатель')
    name = models.CharField(verbose_name='Название', max_length=255)
    country = models.CharField('страна', max_length=128, blank=True, default='')



    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Работодатель'
        verbose_name_plural = 'Работодатели'


class Vacancy(models.Model):

    LANGUAGE_CHOICES = (
        ('de', 'Немецкий'),
        ('ru', 'Руский'),
        ('en', 'Английский'),
    )

    PROFICIENCY_LEVELS = (
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
    )

    EXCHANGE = (
        ('RUB','RUB'),
        ('USD','USD'),
        ('EUR','EUR'),
        ('KGS','KGS'),
        ('KZT','KZT'),
    )

    language = models.CharField('Язык', choices=LANGUAGE_CHOICES, max_length=2, blank=True, default='')
    proficiency = models.CharField('Уровень владения', choices=PROFICIENCY_LEVELS, max_length=2, blank=True, default='')

    ACCOMODATION_TYPE_CHOICES = (
        ('yes', 'Предоставляется'),
        ('no', 'Не предоставляется'),
    )
    picture = models.ImageField(upload_to='vacancy_pics/', blank=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name='Работодатель')
    employer_company = models.ForeignKey(EmployerCompany, verbose_name='Компания работодателя',
                                         on_delete=models.CASCADE, related_name='vacancies')

    required_positions = models.PositiveIntegerField('Требуемое количество мест', default=1)
    required_positions_reviews = models.PositiveIntegerField('Колличество одобренных вакансии', default=0)
    exchange = models.CharField(max_length=10, choices=EXCHANGE, default='', blank=True )
    name = models.CharField('Название вакансии', max_length=255)
    salary = models.CharField('Зарплата', max_length=128)
    duty = models.TextField('Обязанности работника', blank=True, default='')
    city = models.CharField('Город', max_length=128, blank=True, default='')
    accomodation_type = models.CharField('Жилье', choices=ACCOMODATION_TYPE_CHOICES, max_length=50,
                                         default='', blank=True)
    accomodation_cost = models.CharField('Стоимость жилья', max_length=128, blank=True, default='')
    is_vacancy_confirmed = models.BooleanField('Прошел на вакансию', default=False)
    insurance = models.BooleanField('Страховка', default=False)
    transport = models.CharField('Транспорт', max_length=128, blank=True, default='')
    contact_info = models.TextField('Контактные данные', blank=True, default='')
    destination_point = models.TextField('Пункт назначения', blank=True, default='')
    employer_dementions = models.CharField('Требования работодателя', max_length=128, blank=True, default='')
    extra_info = models.CharField('Доп. информация', max_length=255, blank=True, default='')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.name
    
    def is_new(self):
        delta = timezone.now() - self.created_date
        return delta <= timedelta(hours=12)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class ReviewVacancy(models.Model):
    PROFILE_CHOICES = (
        ('Одобрено', 'Одобрено'),
        ('На рассмотрении', 'На рассмотрении'),
        ('Отказано', 'Отказано'),
    )

    status = models.CharField('Статус отклика', choices=PROFILE_CHOICES, max_length=20, blank=True, default='На рассмотрении')
    applicant_profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, verbose_name='Профиль соискателя')
    employer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name='Работодатель')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, verbose_name='Вакансия')
    employer_comment = models.TextField('Комментарий работодателя', blank=True, default='')

    def str(self):
        return f'{self.applicant_profile.user}-{self.vacancy.name}'

    class Meta:
        verbose_name = 'Отклик на вакансию'
        verbose_name_plural = 'Отклики на вакансии'



class Invitation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает ответа'),
        ('accepted', 'Принято'),
        ('declined', 'Отклонено')
    ]

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="invitations")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    employer = models.ForeignKey(EmployerCompany, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user} - {self.vacancy}"


class CompanyReview(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )

    company = models.ForeignKey(EmployerCompany, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name='Пользователь')  # Предполагается, что отзыв может оставить зарегистрированный пользователь
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, verbose_name='Рейтинг')
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    is_review_confirmed = models.BooleanField('Прошел модерацию', default=False)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def str(self):
        return f"{self.company} - {self.rating} Stars"

    class Meta:
        verbose_name = 'Отзыв о компании'
        verbose_name_plural = 'Отзывы о компаниях'







class ProfileCounter(models.Model):

    amount_of_profiles = models.IntegerField('Количество зарегистрированных пользователей', default=0)
    list_of_names = ArrayField(models.CharField(max_length=120), blank=True, null=True)
    creation_date = models.DateField(verbose_name='Дата')

    def __str__(self):
        return str(self.creation_date)

    class Meta:
        verbose_name = 'Количество зарег-ых пользователей'
        verbose_name_plural = 'Количество зарег-ых пользователей'


class Tariff(models.Model):
    amount_in_digits = models.IntegerField(verbose_name='Сумма цифрами', default=10000, null=True)
    amount_in_text = models.CharField(verbose_name='Сумма буквами', max_length=128, default='десять тысяч', null=True)

    # Варианты тарифов
    TARIF_CHOICES = [
        (10000, 'Десять тысяч'),
        (20000, 'Двадцать тысяч'),
        (35000, 'Тридцать пять тысяч'),
    ]

    amount_choice = models.IntegerField('Вариант тарифа', choices=TARIF_CHOICES, default=10000)

    def __str__(self):
        return self.amount_in_text

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
