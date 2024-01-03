from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.utils.translation import gettext, gettext_lazy as _
from ckeditor.fields import RichTextField

# class Event(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='events'
#     )

#     def __str__(self):
#         return self.title
    
#     class Meta:
#         verbose_name = _('Календарь')
#         verbose_name_plural = _('Календарь')

class University(models.Model):
    name = models.CharField(_('Название'), max_length=500)
    name_ru = models.CharField(_('Название на русском'), max_length=500)
    name_de = models.CharField(_('Название на немецком'), max_length=500)
    address = RichTextField(_('Адрес на немецком'))
    phone = models.CharField(_('Номер телефона'), max_length=50)
    site = models.URLField(_('Сайт университета'))

    class Meta:
        ordering = ['name_ru', ]
        verbose_name = _('университет')
        verbose_name_plural = _('университеты')

    def __str__(self):
        return self.name_ru


class Faculty(models.Model):
    name_ru = models.CharField(_('Название на русском'), max_length=500)
    name_de = models.CharField(_('Название на немецком'), max_length=500)

    class Meta:
        ordering = ['name_ru', ]
        verbose_name = _('факультет')
        verbose_name_plural = _('факультеты')

    def __str__(self):
        return self.name_ru


class Notification(models.Model):
    profile = models.ForeignKey('accounts.Profile', on_delete=models.SET_NULL, verbose_name=_('Пользователь'),
                                related_name='notifications', blank=True, null=True)
    author = models.CharField(_('Автор'), default='iWEX', max_length=500)
    title = models.CharField(_('Заголовок'), default='Сообщение', max_length=500)
    message = models.CharField(_('Сообщение'), max_length=1000)
    date = models.DateTimeField(_('Время отправки'), auto_now_add=True)
    is_viewed = models.BooleanField(_('Просмотрено'), default=False)

    class Meta:
        ordering = ['-date', ]
        verbose_name = _('уведомление')
        verbose_name_plural = _('уведомления')

    def __str__(self):
        return self.title


class ContractAdmin(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, _('Мужской')),
        (FEMALE, _('Женский')),
    )

    first_name = models.CharField(_('Имя'), max_length=500, default='')
    last_name = models.CharField(_('Фамилия'), max_length=500, default='')
    father_name = models.CharField(_('Отчество'), max_length=500, default='', blank=True)
    gender = models.CharField(_('Пол'), choices=GENDER_CHOICES, max_length=1, default=MALE)
    patent_id = models.CharField(_('Номер патента (N1234567)'), max_length=20, default='')
    patent_date = models.DateField(_('Дата получения патента'))
    given_by = RichTextField(_('Выдан (УГНС по Ленинскому району)'))

    class Meta:
        ordering = ['id', ]
        verbose_name = _('Администратор для контрактов')
        verbose_name_plural = _('Администраторы для контрактов')

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        full_name = f'{self.last_name} {self.first_name}'
        full_name = f'{full_name} {self.father_name}' if self.father_name else full_name
        return full_name



class EmployerCompany(models.Model):
    icon = models.ImageField(upload_to='company_icons/', blank=True, verbose_name=_('Изображение'))
    # image_back = models.ImageField(upload_to='company_image_back/', blank=True, null=True, verbose_name='изображение')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, blank=True, verbose_name=_('Работодатель'))
    name = models.CharField(verbose_name=_('Название'), blank=True, max_length=255)
    country = models.CharField(_('страна'), max_length=128, blank=True, default='')
    description = RichTextField(_('Описание'), blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Работодатель')
        verbose_name_plural = _('Работодатели')

class CompanyReview(models.Model):
    RATING_CHOICES = (
        (1, _('1 звезда')),
        (2, _('2 звезды')),
        (3, _('3 звезды')),
        (4, _('4 звезды')),
        (5, _('5 звезд'))
    )

    company = models.ForeignKey(EmployerCompany, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('Компания'))
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('Пользователь'))  # Предполагается, что отзыв может оставить зарегистрированный пользователь
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, verbose_name=_('Рейтинг'))
    comment = RichTextField(verbose_name=_('Комментарий'), blank=True)
    is_review_confirmed = models.BooleanField(verbose_name=_('Прошел модерацию'), default=False)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата публикации'))

    def str(self):
        return f"{self.company} - {self.rating} звезд"

    class Meta:
        verbose_name = _('Отзыв о компании')
        verbose_name_plural = _('Отзывы о компаниях')


class Category(models.Model):
    name = models.CharField(_('Категория'), max_length=255, db_index=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Категория'), related_name='subcategories')
    name = models.CharField(_('Подкатегория'), max_length=255, db_index=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Подкатегория')
        verbose_name_plural = _('Подкатегории')



class Vacancy(models.Model):

    LANGUAGE_CHOICES = (
        ('de', _('Немецкий')),
        ('ru', _('Руский')),
        ('en', _('Английский')),
    )

    PROFICIENCY_LEVELS = (
        ('A1', _('A1')),
        ('A2', _('A2')),
        ('B1', _('B1')),
        ('B2', _('B2')),
        ('C1', _('C1')),
        ('C2', _('C2')),
    )

    EXCHANGE = (
        ('RUB', _('RUB')),
        ('USD', _('USD')),
        ('EUR', _('EUR')),
        ('KGS', _('KGS')),
        ('KZT', _('KZT')),
    )

    language = models.CharField(_('Язык'), choices=LANGUAGE_CHOICES, max_length=2, blank=True, default='')
    proficiency = models.CharField(_('Уровень владения'), choices=PROFICIENCY_LEVELS, max_length=2, blank=True, default='')

    ACCOMODATION_TYPE_CHOICES = (
        ('yes', _('Предоставляется')),
        ('no', _('Не предоставляется')),
    )
    picture = models.ImageField(upload_to='vacancy_pics/', blank=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('Работодатель'))
    employer_company = models.ForeignKey(EmployerCompany, verbose_name=_('Компания работодателя'),
                                         on_delete=models.CASCADE, related_name='vacancies')

    required_positions = models.PositiveIntegerField(_('Требуемое количество мест'), default=1)
    required_positions_reviews = models.PositiveIntegerField(_('Колличество одобренных вакансии'), default=0)
    exchange = models.CharField(max_length=10, choices=EXCHANGE, default='', blank=True)
    name = models.CharField(_('Название вакансии'), max_length=255)
    salary = models.IntegerField(_('Зарплата'), )
    duty = RichTextField(_('Обязанности работника'), blank=True, default='')
    city = models.CharField(_('Город'), max_length=128, blank=True, default='')
    accomodation_type = models.CharField(_('Жилье'), choices=ACCOMODATION_TYPE_CHOICES, max_length=50,
                                         default='', blank=True)
    accomodation_cost = models.CharField(_('Стоимость жилья'), max_length=128, blank=True, default='')
    is_vacancy_confirmed = models.BooleanField(_('Прошел на вакансию'), default=False)
    insurance = models.BooleanField(_('Страховка'), default=False)
    transport = models.CharField(_('Транспорт'), max_length=128, blank=True, default='')
    contact_info = models.CharField(_('Контактные данные'), max_length=100,blank=True, default='')
    destination_point = RichTextField(_('Пункт назначения'), blank=True, default='')
    employer_dementions = models.CharField(_('Требования работодателя'), max_length=128, blank=True, default='')
    extra_info = models.CharField(_('Доп. информация'), max_length=255, blank=True, default='')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата публикации'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Категория'), db_index=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Подкатегория'), db_index=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Вакансия')
        verbose_name_plural = _('Вакансии')


class ReviewVacancy(models.Model):
    PROFILE_CHOICES = (
        ('Одобрено', _('Одобрено')),
        ('На рассмотрении', _('На рассмотрении')),
        ('Отказано', _('Отказано')),
    )

    status = models.CharField(_('Статус отклика'), choices=PROFILE_CHOICES, max_length=20, blank=True, default=_('На рассмотрении'))
    applicant_profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, verbose_name=_('Профиль соискателя'))
    employer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('Работодатель'))
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, verbose_name=_('Вакансия'))
    employer_comment = RichTextField(_('Комментарий работодателя'), blank=True, default='')

    def __str__(self):
        return f'{self.applicant_profile.user}-{self.vacancy.name}'

    class Meta:
        verbose_name = _('Отклик на вакансию')
        verbose_name_plural = _('Отклики на вакансии')

        


class ProfileCounter(models.Model):

    amount_of_profiles = models.IntegerField(_('Количество зарегистрированных пользователей'), default=0)
    list_of_names = ArrayField(models.CharField(max_length=120), blank=True, null=True)
    creation_date = models.DateField(verbose_name=_('Дата'))

    def __str__(self):
        return str(self.creation_date)

    class Meta:
        verbose_name = _('Количество зарегистрированных пользователей')
        verbose_name_plural = _('Количество зарегистрированных пользователей')


class Tariff(models.Model):

    amount_in_digits = models.IntegerField(verbose_name=_('Сумма цифрами'), default=10000, null=True)
    amount_in_text = models.CharField(verbose_name=_('Сумма буквами'), max_length=128, default='десять тысяч', null=True)

    def __str__(self):
        return self.amount_in_text

    class Meta:
        verbose_name = _('Тариф')
        verbose_name_plural = _('Тарифы')


class Invitation(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Ожидает ответа')),
        ('accepted', _('Принято')),
        ('declined', _('Отклонено'))
    ]

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="invitations")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    employer = models.ForeignKey(EmployerCompany, on_delete=models.CASCADE)
    message = RichTextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def str(self):
        return f"{self.user} - {self.vacancy}"

    class Meta:
        verbose_name = _('Приглашение на вакансию')
        verbose_name_plural = _('Приглашения на вакансии')



class Feedback(models.Model):
    STATUS_CHOICES = (
        ('MODERETED', _('Прошел модерацию')),
        ('IN_PROCESS', _('В обработке')),
        ('DECLINED', _('Отклонен')),
    )
    text = RichTextField(verbose_name=_('Текст отзыва'))
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='IN_PROCESS', verbose_name=_('Статус'))

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')

class ImprovementIdea(models.Model):
    STATUS_CHOICES = (
        ('NEW', _('Новый')),
        ('IN_PROCESS', _('В обработке')),
        ('IMPLEMENTED', _('Реализован')),
        ('DECLINED', _('Отклонен')),
    )
    text = RichTextField(verbose_name=_('Текст идеи'))
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='NEW', verbose_name=_('Статус'))

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = _('Идея улучшения')
        verbose_name_plural = _('Идеи улучшения')



