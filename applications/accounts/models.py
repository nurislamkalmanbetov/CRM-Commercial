import datetime
import json
import uuid
from datetime import date, timedelta

from applications.accounts.managers import (ProfileEssentialInfoManager,
                                            ProfileInArchiveManager,
                                            ProfileInEmbassyManager,
                                            ProfileInInterviewManager,
                                            ProfileInRegistrationManager,
                                            ProfileInSendingManager,
                                            ProfileInTerminManager,
                                            ProfileInVacancyManager,
                                            ProfileNotConfirmedManager,
                                            ProfileRefusedManager,
                                            StaffManager, UserManager)
from applications.accounts.utils import user_directory_path
from applications.core.models import (EmployerCompany, Faculty, ProfileCounter,
                                      University, Vacancy)
from django.contrib.admin.models import LogEntry
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_image_file_extension
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils import FieldTracker
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey
from ckeditor.fields import RichTextField



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email адрес'), unique=True, db_index=True)
    phone = models.CharField(_('Номер телефона'), max_length=50, blank=True, db_index=True)
    whatsapp_phone = models.CharField(_('Номер Whatsapp'), max_length=50, blank=True, db_index=True)
    is_employer = models.BooleanField(_('Работадатель'), default=False)
    is_staff = models.BooleanField(_('Сотрудник'), default=False)
    is_student = models.BooleanField(_('Студент'), default=False)
    is_superuser = models.BooleanField(_('Суперпользователь'), default=False)
    is_active = models.BooleanField(_('Активен'), default=True)
    is_delete = models.BooleanField(_('Удален'), default=False)
    is_verified_email = models.BooleanField('Почта подтверждена', default=False)
    verification_code = models.CharField('Код подтверждения', max_length=6, blank=True, null=True)
    verification_code_created_at = models.DateTimeField('Дата создания кода подтверждения', blank=True, null=True)
    registered_at = models.DateTimeField(_('Дата регистрации'), auto_now_add=True)
    password_reset_token = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.email:
            raise ValueError('User must have an email')
        # if self.pk is None:  # если это новый объект
        #     self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.is_superuser:
            self.is_delete = True
            self.save()
        else:
            super(User, self).delete(*args, **kwargs)
            
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')


def get_due_date():
    return date.today() + timedelta(days=60)


def is_staff_or_superuser(user_id):
    user = User.objects.get(pk=user_id)
    if not user.is_staff and not user.is_superuser:
        raise ValidationError("Only staff or superuser can be assigned as 'Оплату принял'")


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    who_created = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('Оплату принял'), related_name='payments_received', validators=[is_staff_or_superuser])
    amount_paid = models.DecimalField(_('Оплачено'), max_digits=10, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(_('Остаток'), max_digits=10, decimal_places=2, editable=False, default=35000)
    is_fully_paid = models.BooleanField(_('Оплачено полностью'), default=False)
    payment_date = models.DateField(_('Дата оплаты'), auto_now_add=True)
    due_date = models.DateField(_('Крайний срок оплаты'), default=get_due_date, null=True)

    def __str__(self):
        return f"ID: {self.id} {self.user.email} Оплачено: {self.amount_paid} Остаток: {self.remaining_amount}"

    def save(self, *args, **kwargs):
        # Вычисляем остаток на основе оплаченной суммы
        self.remaining_amount = 35000 - self.amount_paid
        # Устанавливаем значение is_fully_paid в зависимости от остатка
        self.is_fully_paid = self.remaining_amount <= 0
        # Если запись создается (и не обновляется), устанавливаем due_date на 2 месяца позже от текущей даты
        if not self.pk:  # Проверка, что объект еще не сохранен в базе данных
            self.payment_date = date.today()
            if self.is_fully_paid:
                self.due_date = None
            else:
                self.due_date = self.payment_date + timedelta(days=60)  # Добавляем 60 дней (приближенно 2 месяца)
        super(Payment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Платеж студента')
        verbose_name_plural = _('Платежи студентов')


class Staff(User):
    objects = StaffManager()

    class Meta:
        proxy = True
        verbose_name = _('сотрудник')
        verbose_name_plural = _('сотрудники')


class Profile(models.Model):

    GENDER_CHOICES = (
        ("M", _("Мужской")),
        ("F", _("Женский")),
    )

    NATIONALITY_CHOICES = (
        ('Кыргызстан', _('Кыргызстан')),
        ('Казахстан', _('Казахстан')),
        ('Узбекистан', _('Узбекистан')),
        ('Таджикистан', _('Таджикистан')),
        ('Россия', _('Россия')),
        ('другое', _('другое')),
    )

    COUNTRY_CHOICES = (
        ('Кыргызстан', _('Кыргызстан')),
        ('Казахстан', _('Казахстан')),
        ('Узбекистан', _('Узбекистан')),
        ('Таджикистан', _('Таджикистан')),
        ('Россия', _('Россия')),
        ('Türkei', _('Турция')),
    )

    REGION_CHOICES = (
        ("Tschui", _("Чуйская область")),
        ("Naryn", _("Нарынская область")),
        ("Talas", _("Таласская область")),
        ("Issik-Kul", _("Ыссык-Кульская область")),
        ("Zhalal-Abad", _("Жалал-Абадская область")),
        ("Osh", _("Ошская область")),
        ("Batken", _("Баткенская область")),
    )

    REGION_CHOICES_RU = (
        ("Чуйская область", _("Чуйская область")),
        ("Нарынская область", _("Нарынская область")),
        ("Таласская область", _("Таласская область")),
        ("Ыссык-Кульская область", _("Ыссык-Кульская область")),
        ("Жалал-Абадская область", _("Жалал-Абадская область")),
        ("Ошская область", _("Ошская область")),
        ("Баткенская область", _("Баткенская область")),
    )

    DEGREE_CHOICES = (
        ("бакалавр", _("Бакалавр")),
        ("магистр", _("Магистр")),
        ("колледж", _("Колледж")),
    )

    YEAR_CHOICES = [(i, i) for i in range(1, 6)]

    POSITION_CHOICES = (
        ("Kellner", _("Официант")),
        ("Verkäufer", _("Продавец")),
        ("Kassierer", _("Кассир")),
        ("Küchenhelfer", _("Кух. работник")),
        ("Zimmermädchen", _("Горничная")),
        ("Rezeptionist", _("Ресепшн")),
        ("Lager", _("Грузчик")),
        ("Taxifahrer", _("Таксист")),
        ("Lehrer", _("Преподаватель")),
        ("Kinderfrau", _("Няня")),
        ("Bote", _("Курьер")),
        ("Sekretär", _("Секретарь")),
        ("Feldarbeiter", _("Работа на полях")),
        ("Call-Center-Betreiber", _("Оператор call-центра")),
        ("Wächter", _("Охранник")),
        ("Promoter", _("Промоутер")),
        ("Barmann", _("Бармен")),
        ("Reiseführer", _("Гид")),
        ("Animateur", _("Аниматор")),
        ("Tankwagen", _("Заправщик")),
        ("Verwalter", _("Администратор")),
        ("Packer", _("Упаковщик")),
        ("Nähwerkarbeiter", _("Работа в швейном цеху")),
        ("Putzfrau", _("Уборщица")),
        ("Hirt", _("Пастух")),
        ("Bauernarbeiter", _("Работа на фермах")),
        ("Sanitäter", _("Санитар")),
        ("Bauarbeiter", _("Строитель")),
        ("Visagist", _("Визажист")),
        ("Designer", _("Дизайнер")),
        ("Haushälterin", _("Домохозяйка")),
        ("Lagerverwalter", _("Кладовщик")),
        ("Absatzforscher", _("Маркетолог")),
        ("Masseur", _("Массажист")),
        ("Möbelbauer", _("Мебельщик")),
        ("Krankenpfleger", _("Медбрат")),
        ("Krankenschwester", _("Медсестра")),
        ("Manager", _("Мэнеджер")),
        ("Monteur", _("Монтёр")),
        ("Operator", _("Оператор")),
        ("Finisher", _("Отделочник")),
        ("Friseur", _("Парикмахер")),
        ("Übersetzer", _("Переводчик")),
        ("Koch", _("Повар")),
        ("Geschirrspüler", _("Посудомойщик")),
        ("Briefträger",_("Почтальон")),
        ("Wäscherin", _("Прачка")),
        ("Lagerarbeiter", _("Работа на складах")),
        ("Hilfsarbeiter", _("Разнорабочий")),
        ("Installateur", _("Сантехник")),
        ("Schweißer", _("Сварщик")),
        ("Krankenpflegerin", _("Сиделка")),
        ("Handelsvertreter", _("Торговый агент")),
        ("Trainer", _("Тренер")),
        ("Raumpfleger", _("Уборщик")),
        ("Fotograf", _("Фотограф")),
        ("Choreograph", _("Хореограф")),
        ("Elektriker", _("Хореограф")),
    )

    WORK_COUNTRY_CHOICES = (
        ('Кыргызстан', _('Кыргызстан')),
        ('Россия', _('Россия')),
        ('Турция', _('Турция')),
        ('Казахстан', _('Казахстан')),
        ('Германия', _('Германия')),
        ('Узбекистан', _('Узбекистан')),
        ('Таджикистан', _('Таджикистан')),
        ('Дубай', _('Дубай')),
        ('USA', _('Америка')),
        ('другое', _('другое')),
    )

    LANGUAGE_LEVEL_CHOICES = (
        ('C2', _('В совершенстве')),
        ('C1', _('Очень хорошо')),
        ('B2', _('Хорошо')),
        ('B1', _('Разговорный')),
        ('A2', _('Обучаюсь')),
        ('A1', _('Начальный')),
        ('0', _('Не знаю')),
)



    DRIVING_EXPERIENCE_CHOICES = (
        ("1", _("до 1 года")),
        ("2", _("1 год")),
        ("3", _("2 года")),
        ("4", _("3 года")),
        ("5", _("4 и более лет")),
    )

    TRANSMISSION_CHOICES = (
        ("1", _("Механика")),
        ("2", _("Автомат")),
        ("3", _("Механика и автомат")),
    )

    SHIRT_SIZE_CHOICES = (
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
    )

    PANTS_SIZE_CHOICES = [(i, i) for i in range(24, 37)]
    SHOE_SIZE_CHOICES = [(i, i) for i in range(34, 47)]

    LEVEL_CHOICES = (
        ('a0', 'A0'),
        ('a1', 'A1'),
        ('a1+', 'A1+'),
        ('a2', 'A2'),
        ('a2+', 'A2+'),
        ('b1', 'B1'),
        ('b1+', 'B1+'),
        ('b2', 'B2'),
        ('b2+', 'B2+'),
        ('c1', 'C1'),
    )

    BICYCLE_SKILL_CHOICES = (
        ("ride_good", _("Да, отлично")),
        ("ride_bad", _("Да, но плохо")),
        ("cant_ride", _("Нет, не умею")),
    )

    ACCOMODATION_TYPE_CHOICES = (
        ("student", _("Студент")),
        ("employer", _("Работодатель")),
    )

    EMBASSY_VISAMETRIC_CHOICES = (
        ("embassy", _("Посольство")),
        ("visametric", _("Визаметрик")),
    )

    MARSHRUT_CHOICES = (
        ("not_exist", _("Нет маршрута")),
        ("doubtful", _("Сомнительно")),
        ("created", _("Маршрут был составлен")),
        ("received", _("Маршрут был получен")),
    )

    DOMKOM_DOC_CHOICES = (
        ("not_exist", _("Нет")),
        ("brought", _("Принес")),
        ("sent", _("Отправили в Германию")),
        ("not_given", _("Не дали")),
    )

    BILET_DOC_CHOICES = (
        ("not_exist", _("Нет")),
        ("brought", _("Принес")),
        ("sent", _("Отправили в Германию")),
        ("not_given", _("Не смог получить (сомнительно)")),
    )
    DIRECTION_CHOICES = (
        ('nord', 'Nord'),
        ('sud', 'Süd')
    )

    user = models.OneToOneField(User, models.CASCADE, related_name='profile')
    photo = models.ImageField(_('Фотография'),upload_to='media/profile', blank=True, null=True)
    # main questionnaire confirmation
    is_confirmed = models.BooleanField(_('Подтвержден пользователем'), default=False)
    is_form_completed = models.BooleanField(_('Статус заполнения формы'), default=False)
    is_admin_confirmed = models.BooleanField(_('Подтверждено админом'), default=False)
    access_to_registration_documents = models.BooleanField(_('Доступ к справкам для регистрации'), default=False)
    access_to_embassy_documents = models.BooleanField(_('Доступ к справкам для посольства'), default=False)
    start_vise_date = models.DateField(_('Дата начала действия визы'), blank=True, default=None, null=True)
    end_vise_date = models.DateField(_('Дата окончания действия визы'), blank=True, default=None, null=True)
    level = models.CharField(
        _("Уровень"), choices=LEVEL_CHOICES, max_length=20, default="", blank=True
    )
    courses_info = RichTextField(_("Курсы"), default="", blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    comment = RichTextField(_("Комментарий"), default="", blank=True)
    note = models.CharField(_("Заметка"), default="", blank=True, max_length=255)

    # personal info
    first_name = models.CharField(
        _("Имя на латинице"), max_length=255, default="", blank=True
    )
    first_name_ru = models.CharField(
        _("Имя на кириллице"), max_length=255, default="", blank=True
    )
    last_name = models.CharField(
        _("Фамилия на латинице"), max_length=255, default="", blank=True
    )
    last_name_ru = models.CharField(
        _("Фамилия на кирилице"), max_length=255, default="", blank=True
    )
    gender = models.CharField(
        _("Пол"), choices=GENDER_CHOICES, max_length=20, default="", blank=True
    )
    bday = models.DateField(_("День рождения"), null=True, blank=True)
    nationality = models.CharField(
        _("Гражданство"),
        choices=NATIONALITY_CHOICES,
        max_length=50,
        default="",
        blank=True,
    )
    been_to_germany = models.BooleanField(_("Был в Германии"), blank=True, null=True)

    # birth place
    birth_country = models.CharField(_('Страна рождения'), choices=COUNTRY_CHOICES, max_length=50, default='', blank=True)
    birth_region = models.CharField(_('Область рождения'), choices=REGION_CHOICES, max_length=50, default='', blank=True)
    birth_city = models.CharField(_('Город/cело рождения'), max_length=255, default='', blank=True)

    # place of residence
    reg_region = models.CharField('Область (адрес прописки)', choices=REGION_CHOICES_RU, max_length=50, default='', blank=True)
    reg_city = models.CharField('Город/село на русском (адрес прописки)', max_length=255, default='', blank=True)
    reg_city_en = models.CharField('Город/село на латинице (адрес прописки)', max_length=255, default='', blank=True)
    reg_district = models.CharField('Район на русском (адрес прописки)', max_length=255, default='', blank=True)
    reg_district_en = models.CharField('Район на латинице (адрес прописки)', max_length=255, default='', blank=True)
    reg_street = models.CharField('Улица или микрорайон на русском (адрес прописки)', max_length=500, default='', blank=True)
    reg_street_en = models.CharField('Улица или микрорайон на латинице (адрес прописки)', max_length=500, default='', blank=True)
    reg_house = models.CharField('Дом (адрес прописки)', max_length=255, default='', blank=True)
    reg_apartment = models.CharField(_('Квартира (адрес прописки)'), max_length=255, default='', blank=True)

    # actual address
    live_region = models.CharField('Область (фактический адрес)', choices=REGION_CHOICES_RU, max_length=50, default='', blank=True)
    live_city = models.CharField('Город/село на русском (фактический адрес)', max_length=255, default='', blank=True)
    live_city_en = models.CharField('Город/село на латинице (фактический адрес)', max_length=255, default='', blank=True)
    live_district = models.CharField('Район на русском (фактический адрес)', max_length=255, default='', blank=True)
    live_district_en = models.CharField('Район на латинице (фактический адрес)', max_length=255, default='', blank=True)
    live_street = models.CharField('Улица или микрорайон на русском (фактический адрес)', max_length=500, default='', blank=True)
    live_street_en = models.CharField('Улица или микрорайон на латинице (фактический адрес)', max_length=500, default='', blank=True)
    live_house = models.CharField('Дом (фактический адрес)', max_length=255, default='', blank=True)
    live_apartment = models.CharField('Квартира (фактический адрес)', max_length=255, default='', blank=True)

    # passport data
    passport_number = models.CharField('Номер id паспорта', max_length=100, default='', blank=True)
    zagranpassport_number = models.CharField('Номер загранпаспорта', max_length=100, default='', blank=True)
    zagranpassport_end_time = models.DateField('Дата окончания загранпаспорта', blank=True, null=True)

    # education info
    university = models.ForeignKey(University, on_delete=models.SET_NULL, verbose_name=_('Университет'), related_name='students', blank=True, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, verbose_name=_('Факультет'), related_name='students', blank=True, null=True)
    degree = models.CharField('Академическая степень', choices=DEGREE_CHOICES, max_length=20, default='', blank=True)
    year = models.IntegerField('Курс', choices=YEAR_CHOICES, blank=True, null=True)
    study_start = models.DateField(_('Дата поступления'), blank=True, null=True)
    study_end = models.DateField(_('Дата окончания'), blank=True, null=True)
    summer_holidays_start = models.DateField('Дата начала каникул', blank=True, null=True)
    summer_holidays_end = models.DateField('Дата окончания каникул', blank=True, null=True)
    direction = models.CharField(_('Направление'), max_length=50, blank=True, null=True, choices=DIRECTION_CHOICES)

    # parents info
    father_phone = models.CharField('Контактный номер отца', max_length=50, blank=True, db_index=True)
    father_work_phone = models.CharField('Рабочий номер отца', max_length=50, blank=True, db_index=True)
    father_company = models.CharField('Место работы отца', max_length=255, blank=True)

    mother_phone = models.CharField('Контактный номер матери', max_length=50, blank=True, db_index=True)
    mother_work_phone = models.CharField('Рабочий номер матери', max_length=50, blank=True, db_index=True)
    mother_company = models.CharField('Место работы матери', max_length=255, blank=True)

    # work experience
    # 1 place of work
    company1 = models.CharField('Компания (1 место работы)', max_length=255, default='', blank=True)
    position1 = models.CharField('Должность (1 место работы)', choices=POSITION_CHOICES, max_length=50, default='', blank=True)
    start_date1 = models.DateField('Период работы от (1 место работы)', blank=True, null=True)
    end_date1 = models.DateField('Период работы до (1 место работы)', blank=True, null=True)
    country1 = models.CharField('Страна (1 место работы)', choices=WORK_COUNTRY_CHOICES, max_length=50, default='', blank=True)

    # 2 place of work
    company2 = models.CharField('Компания (2 место работы)', max_length=255, default='', blank=True)
    position2 = models.CharField('Должность (2 место работы)', choices=POSITION_CHOICES, max_length=50, default='', blank=True)
    start_date2 = models.DateField('Период работы от (2 место работы)', blank=True, null=True)
    end_date2 = models.DateField('Период работы до (2 место работы)', blank=True, null=True)
    country2 = models.CharField('Страна (2 место работы)', choices=WORK_COUNTRY_CHOICES, max_length=50, default='', blank=True)

    # 3 place of work
    company3 = models.CharField('Компания (3 место работы)', max_length=255, default='', blank=True)
    position3 = models.CharField('Должность (3 место работы)', choices=POSITION_CHOICES, max_length=50, default='', blank=True)
    start_date3 = models.DateField('Период работы от (3 место работы)', blank=True, null=True)
    end_date3 = models.DateField('Период работы до (3 место работы)', blank=True, null=True)
    country3 = models.CharField('Страна (3 место работы)', choices=WORK_COUNTRY_CHOICES, max_length=50, default='', blank=True)

    # languages info
    german = models.CharField(_('Знание немецкого языка'), choices=LANGUAGE_LEVEL_CHOICES, max_length=150, default='', blank=True)
    english = models.CharField(_('Знание английского языка'), choices=LANGUAGE_LEVEL_CHOICES, max_length=150, default='', blank=True)
    turkish = models.CharField(_('Знание турецкого языка'), choices=LANGUAGE_LEVEL_CHOICES, max_length=150, default='', blank=True)
    russian = models.CharField(_('Знание русского языка'), choices=LANGUAGE_LEVEL_CHOICES, max_length=150, default='', blank=True)
    chinese = models.CharField(_('Знание китайского языка'), choices=LANGUAGE_LEVEL_CHOICES, max_length=150, default='', blank=True)

    # driver license
    driver_license = models.BooleanField(_('Водительские права'), default=False)
    driving_experience = models.CharField(_('Стаж вождения'), choices=DRIVING_EXPERIENCE_CHOICES, max_length=1, default='', blank=True)
    cat_a = models.BooleanField(_("Категория A"), default=False)
    cat_b = models.BooleanField(_("Категория B"), default=False)
    cat_c = models.BooleanField(_("Категория C"), default=False)
    cat_d = models.BooleanField(_("Категория D"), default=False)
    cat_e = models.BooleanField(_("Категория E"), default=False)
    tractor = models.BooleanField(_('Трактор'), default=False)
    transmission = models.CharField(_('Коробка передач'), choices=TRANSMISSION_CHOICES, max_length=1, default='', blank=True)

    # bicycle skills
    bicycle_skill = models.CharField('Умение кататься на велосипеде', choices=BICYCLE_SKILL_CHOICES, max_length=10, default='', blank=True)

    # uniform sizes
    shirt_size = models.CharField('Размер рубашки', choices=SHIRT_SIZE_CHOICES, max_length=3, default='', blank=True)
    pants_size = models.IntegerField('Размер брюк', choices=PANTS_SIZE_CHOICES, blank=True, null=True)
    shoe_size = models.IntegerField('Размер обуви', choices=SHOE_SIZE_CHOICES, blank=True, null=True)

    # hobbies
    reading = models.BooleanField(_("Чтение"), default=False)
    singing = models.BooleanField(_("Пение"), default=False)
    travelling = models.BooleanField(_("Путешествие"), default=False)
    yoga = models.BooleanField(_("Йога"), default=False)
    dancing = models.BooleanField(_("Танцы"), default=False)
    sport = models.BooleanField(_("Спорт"), default=False)
    drawing = models.BooleanField(_("Рисование"), default=False)
    computer_games = models.BooleanField(_("Компьютерные игры"), default=False)
    guitar = models.BooleanField(_("Игра на гитаре"), default=False)
    films = models.BooleanField(_("Фильмы"), default=False)
    music = models.BooleanField(_("Музыка"), default=False)
    knitting = models.BooleanField(_("Вязание"), default=False)
    cooking = models.BooleanField(_("Готовка"), default=False)
    fishing = models.BooleanField(_("Рыбалка"), default=False)
    photographing = models.BooleanField(_("Фотография"), default=False)

    # documents to upload
    study_certificate = models.FileField('Справка с места учебы', upload_to=user_directory_path, blank=True)
    study_certificate_confirm = models.BooleanField('Справка с места учебы - Подтверждено', default=False)
    study_certificate_paper_confirm = models.BooleanField('Справка с места учебы - бумажная версия', default=False)

    study_certificate_embassy = models.FileField('Справка с места учебы для посольства', upload_to=user_directory_path, blank=True)
    study_certificate_embassy_confirm = models.BooleanField('Справка с места учебы для посольства - Подтверждено', default=False)
    study_certificate_paper_embassy_confirm = models.BooleanField('Справка с места учебы для посольства - бумажная версия', default=False)

    study_certificate_translate_embassy = models.FileField('Перевод справки с места учебы для посольства', upload_to=user_directory_path, blank=True)
    study_certificate_translate_embassy_confirm = models.BooleanField('Перевод справки с места учебы для посольства - Подтверждено', default=False)
    study_certificate_translate_paper_embassy_confirm = models.BooleanField('Перевод справки с места учебы для посольства - бумажная версия', default=False)

    photo_for_schengen = models.FileField('Фото на шенген 3.5x4.5', upload_to=user_directory_path, blank=True,
                                          validators=[validate_image_file_extension, ])
    photo_for_schengen_confirm = models.BooleanField('Фото на шенген - Подтверждено', default=False)
    photo_for_schengen_paper_confirm = models.BooleanField('Фото на шенген - бумажная версия', default=False)

    zagranpassport_copy = models.FileField('Загранпаспорт', upload_to=user_directory_path, blank=True)
    zagranpassport_copy_confirm = models.BooleanField('Загранпасспорт - Подтверждено', default=False)
    zagranpassport_copy_paper_confirm = models.BooleanField('Загранпасспорт - бумажная версия', default=False)

    passport_copy = models.FileField('Копия ID', upload_to=user_directory_path, blank=True)
    passport_copy_confirm = models.BooleanField('Пасспорт - Подтверждено', default=False)
    passport_copy_paper_confirm = models.BooleanField('Пасспорт - бумажная версия', default=False)

    fluorography_express = models.FileField('Флюрография регистрация', upload_to=user_directory_path, blank=True)
    fluorography_express_confirm = models.BooleanField('Флюрография регистрация - Подтверждено', default=False)
    fluorography_express_paper_confirm = models.BooleanField('Флюорография регистрация - бумажная версия',
                                                             default=False)

    fluorography = models.FileField('Флюрография посольство', upload_to=user_directory_path, blank=True)
    fluorography_confirm = models.BooleanField('Флюрография посольство - Подтверждено', default=False)
    fluorography_paper_confirm = models.BooleanField('Флюорография посольство - бумажная версия', default=False)

    immatrikulation = models.FileField('Immatrikulation с печатью университета', upload_to=user_directory_path,
                                       blank=True)
    immatrikulation_download_date = models.DateField('Дата загрузки имматрикуляциона', blank=True, null=True)
    immatrikulation_confirm = models.BooleanField('Immatrikulation с печатью университета - Подтверждено',
                                                  default=False)
    immatrikulation_paper_confirm = models.BooleanField('Immatrikulation - бумажная версия', default=False)

    transcript = models.FileField('Транскрипт оригинал', upload_to=user_directory_path, blank=True)
    transcript_confirm = models.BooleanField('Транскрипт оригинал - Подтверждено', default=False)
    transcript_paper_confirm = models.BooleanField('Транскрипт оригинал - бумажная версия', default=False)

    transcript_translate = models.FileField('Перевод транскрипта', upload_to=user_directory_path, blank=True)
    transcript_translate_confirm = models.BooleanField('Перевод транскрипта - Подтверждено', default=False)
    transcript_translate_paper_confirm = models.BooleanField('Перевод транскрипта - бумажная версия', default=False)

    bank_statement = models.FileField('Выписка с банка', upload_to=user_directory_path, blank=True)
    bank_statement_confirm = models.BooleanField('Выписка с банка - Подтверждено', default=False)
    bank_statement_paper_confirm = models.BooleanField('Выписка с банка -  бумажная версия', default=False)

    conduct_certificate = models.FileField('Справка о несудимости', upload_to=user_directory_path, blank=True)
    conduct_certificate_confirm = models.BooleanField('Справка о несудимости - Подтверждено', default=False)
    conduct_certificate_paper_confirm = models.BooleanField('Справка о несудимости - бумажная версия', default=False)

    mentaldispanser_certificate = models.FileField('Справка с психдиспансера', upload_to=user_directory_path,
                                                   blank=True)
    mentaldispanser_certificate_confirm = models.BooleanField('Справка с психдиспансера - Подтверждено', default=False)
    mentaldispanser_certificate_paper_confirm = models.BooleanField('Справка с психдиспансера - бумажная версия',
                                                                    default=False)

    drugdispanser_certificate = models.FileField('Справка с наркодиспансера', upload_to=user_directory_path, blank=True)
    drugdispanser_certificate_confirm = models.BooleanField('Справка с наркодиспансера - Подтверждено', default=False)
    drugdispanser_certificate_paper_confirm = models.BooleanField('Справка с наркодиспансера - бумажная версия',
                                                                  default=False)

    parental_permission = models.FileField('Разрешение от родителей', upload_to=user_directory_path, blank=True)
    parental_permission_confirm = models.BooleanField('Разрешение от родителей - Подтверждено', default=False)
    parental_permission_paper_confirm = models.BooleanField('Разрешение от родителей - бумажная версия', default=False)

    bank_details = models.FileField('Реквизиты банка', upload_to=user_directory_path, blank=True, null=True)
    bank_details_confirm = models.BooleanField('Реквизиты банка - Подтверждено', default=False)
    bank_details_paper_confirm = models.BooleanField('Реквизиты банка - бумажная версия', default=False)

    # documents paper versions
    jipl_paper_confirm = models.BooleanField('ЖИПЛ - бумажная версия', default=False)
    resume_paper_confirm = models.BooleanField('Резюме - бумажная версия', default=False)
    work_contract_paper_confirm = models.BooleanField('Договор труда - бумажная версия', default=False)
    traning_contract_paper_confirm = models.BooleanField('Договор тренинга - бумажная версия', default=False)
    receipt_paper_confirm = models.BooleanField('Расписка - бумажная версия', default=False)
    embassy_anketa = models.BooleanField('Анкета для посольства', default=False)

    # contract date
    contract_date = models.DateField('Дата с договора', blank=True, null=True)

    # embassy appointment date and time
    termin = models.DateTimeField('Дата и время собеседования в посольстве (termin)', blank=True, null=True)
    embassy_visametric = models.CharField('Посольство / Визаметрик', max_length=100, choices=EMBASSY_VISAMETRIC_CHOICES,
                                          default='', blank=True)

    training_sum = models.IntegerField('Сумма за тренинги', default=0)
    training_sum_stable = models.IntegerField('Сумма за тренинг 6000', default=0)
    employment_sum = models.IntegerField('Сумма за трудоустройство', default=0)
    is_training_sum = models.BooleanField(default=False)
    is_training_sum_stable = models.BooleanField(default=False)
    is_employment_sum = models.BooleanField(default=False)
    full_sum = models.IntegerField('Полная сумма к оплате', default=0)

    employer_confirm_date = models.DateField('Дата подтверждения работодателем', blank=True, null=True)
    zav_send_date = models.DateField('Дата отправки в ZAV', blank=True, null=True)
    work_permit_date = models.DateField('Дата получения рабочего разрешения', blank=True, null=True)
    work_invitation_date = models.DateField('Дата получения приглашения на работу', blank=True, null=True)
    documents_send_date = models.DateField('Дата отправления документов', blank=True, null=True)

    german_insurance = models.BooleanField('Немецкая страховка', default=False)
    local_insurance = models.BooleanField('Местная страховка', default=False)
    accomodation = models.BooleanField('Статус подтверждения жилья', default=False)
    accomodation_type = models.CharField('Тип жилья', choices=ACCOMODATION_TYPE_CHOICES, max_length=50, default='', blank=True)
    german_work_contract = models.BooleanField('Рабочий договор', default=False)

    documents_collected_by = models.CharField('Сбор документов осуществлен админом', max_length=500, default='', blank=True)
    consultant = models.CharField('Консультант', max_length=500, default='', blank=True)
    consult_date = models.DateField('Дата консультации', blank=True, null=True)

    # before sending student
    flight_date = models.DateTimeField('Дата и время вылета в Германию', blank=True, null=True)
    arrival_date = models.DateTimeField('Дата и время прилета в Германию', blank=True, null=True)
    destination_date = models.DateTimeField('Дата и время прибытия в пункт назначения', blank=True, null=True)
    arrival_city = models.CharField('Город - пункт назначения', max_length=500, default='', blank=True)
    arrival_airport = models.CharField('Аэропорт - пункт назначения', max_length=500, default='', blank=True)
    arrival_place = RichTextField('Пункт назначения', default='', blank=True)
    marshrut = models.CharField('Маршрут', choices=MARSHRUT_CHOICES, max_length=30, default='not_exist', blank=True)
    immatrikulation_received = models.BooleanField('Immatrikulation выдан студенту на руки', default=False)
    domkom_document = models.CharField('Справка от домкома', choices=DOMKOM_DOC_CHOICES, max_length=30, default='not_exist', blank=True)
    bilet_document = models.CharField('Билет', choices=BILET_DOC_CHOICES, max_length=30, default='not_exist', blank=True)
    akt_trainings = models.BooleanField('Акт по тренингам', default=False)
    akt_iwex = models.BooleanField('Акт IWEX', default=False)
    receipt_flight = models.BooleanField('Расписка по инструктажу', default=False)
    consultant_before_flight = models.CharField('Консультант (инструктаж перед вылетом)', max_length=500, default='', blank=True)

    # work period based on related interview objects
    work_from = models.DateField('Дата начала работы', blank=True, null=True)
    work_to = models.DateField('Дата окончания работы', blank=True, null=True)

    # company name and position based on related interview object
    company_name = models.CharField('Название компании', max_length=500, blank=True, default='')
    position = models.CharField('Вакансия', max_length=500, blank=True, default='')

    # new agreements for admin users
    agreement1_download_date = models.DateField('Дата загрузки Договора на тренинг',null=True , blank=True)
    agreement2_download_date = models.DateField('Дата загрузки Договора на трудоустройство',null=True,  blank=True)
    agreement3_download_date = models.DateField('Дата загрузки Договора на тренинг 6000', null=True, blank=True)

    agreement1 = models.FileField('Договор на тренинг', upload_to=user_directory_path, blank=True, null=True)
    agreement2 = models.FileField('Договор на трудоустройство', upload_to=user_directory_path, blank=True, null=True)
    agreement3 = models.FileField('Договор на тренинг 6000', upload_to=user_directory_path, blank=True, null=True)

    agreement1_date = models.DateField(null=True, blank=True,)
    agreement2_date = models.DateField(null=True, blank=True,)
    agreement3_date = models.DateField(null=True, blank=True,)

    agreement1_number = models.CharField(max_length=32, null=True, blank=True,)
    agreement2_number = models.CharField(max_length=32, null=True, blank=True,)
    agreement3_number = models.CharField(max_length=32, null=True, blank=True,)

    act1 = models.FileField('Акт приема-передачи №1 (тренинг)', upload_to=user_directory_path, blank=True, null=True)
    act2 = models.FileField('Акт приема-передачи №2(трудоустройство)', upload_to=user_directory_path, blank=True, null=True)
    act3 = models.FileField('Акт приема-передачи №3 (тренинг6000)', upload_to=user_directory_path, blank=True, null=True)

    act1_download_date = models.DateField('Дата загрузки акта тренинги', null=True,  blank=True)
    act2_download_date = models.DateField('Дата загрузки акта №2', null=True,  blank=True)
    act3_download_date = models.DateField('Дата загрузки акта №3', null=True,  blank=True)

    closure1 = models.FileField('Расторжение №1(тренинг)', upload_to=user_directory_path, blank=True, null=True)
    closure2 = models.FileField('Расторжение №2(трудоустройство)', upload_to=user_directory_path, blank=True, null=True)
    closure3 = models.FileField('Расторжение №3(тренинг 6000)', upload_to=user_directory_path, blank=True, null=True)

    consult_list = models.FileField('Консультационный лист', upload_to=user_directory_path, blank=True, null=True)

    # new embassy fields
    invitation = models.FileField('Приглашение', upload_to=user_directory_path, blank=True, null=True)
    labor_agreement = models.FileField('Рабочий договор', upload_to=user_directory_path, blank=True, null=True)
    liveplace_approve = models.FileField('Подтверждение жилья', upload_to=user_directory_path, blank=True, null=True)
    insurance = models.FileField('Страховка', upload_to=user_directory_path, blank=True, null=True)
    in_review = models.BooleanField('На расссмотрении', blank=True, null=True)
    visa_file = models.FileField('Скан визы', upload_to=user_directory_path, blank=True, null=True)
    visa_reject = models.BooleanField('Отказано в визе', blank=True, null=True)
    loan = models.IntegerField('Долг', blank=True, null=True)

    # new vacancy fields
    living_condition = RichTextField('Условия проживания', blank=True, null=True)

    # termin fields
    new_email = models.EmailField('Новая почта', blank=True, null=True)
    telephone = models.CharField('Номер телефона', max_length=128, blank=True, null=True)
    pnr_code = models.CharField('PNR-код', max_length=128, blank=True, null=True)
    termin_scan = models.FileField('Скан термина', upload_to=user_directory_path, blank=True, null=True)
    has_termin = models.BooleanField('Наличие термина', default=False)

    # new personal info
    characteristics = RichTextField('Характеристика', default='', blank=True)
    nvks = models.BooleanField('НВКС', default=False)

    # new interview fields
    in_interview_review = models.BooleanField('На рассмотрении в Собеседовании', blank=True, null=True)
    director_manager = models.ForeignKey(Staff, on_delete=models.SET_NULL, verbose_name='Ответственный менеджер',
                                         related_name='students', blank=True, null=True)

    # new fields in sending
    employer = models.ForeignKey('core.EmployerCompany', verbose_name='Работодатель',
                                 on_delete=models.SET_NULL, related_name='employees', blank=True, null=True)

    # field tracker
    tracker = FieldTracker()

    is_refused = models.BooleanField(verbose_name='Отказался', default=False)

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'

        if self.first_name and not self.last_name:
            return self.first_name

        if not self.first_name and self.last_name:
            return self.last_name
        return self.user.__str__()

    def delete(self, *args, **kwargs):
        self.user.delete()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property 
    def full_name_reverse(self):
        return f'{self.last_name} {self.first_name}'

    @property
    def full_name_ru(self):
        return f'{self.last_name_ru} {self.first_name_ru}'

    @property
    def paid_sum(self):
        if self.bills:
            return sum(x.pay_sum for x in self.bills.all())
        return 0

    @property
    def paid_percent(self):
        if self.full_sum:
            return f'{int(self.paid_sum * 100 / self.full_sum)} %'
        return 'НЕТ СУММЫ К ОПЛАТЕ'

    @property
    def lost_sum(self):
        if self.full_sum:
            return f'{int(self.full_sum - self.paid_sum)} сом'
        return 'НЕТ СУММЫ К ОПЛАТЕ'

    @property
    def get_hobbies(self):

        props = {
            'reading': 'Чтение',
            'singing': 'Пение',
            'travelling': 'Путешествие',
            'yoga': 'Йога',
            'dancing': 'Танцы',
            'sport': 'Спорт',
            'drawing': 'Рисование',
            'computer_games': 'Компьютерные игры',
            'guitar': 'Игра на гитаре',
            'films': 'Фильмы',
            'music': 'Музыка',
            'knitting': 'Вязание',
            'cooking': 'Готовка',
            'fishing': 'Рыбалка',
            'photographing': 'Фотография',
        }

        res = list()

        for k in props.keys():
            if (getattr(self, k)):
                res.append(props[k])

        return res

    @property
    def get_hobbies_de(self):
        props = {
            'reading': 'Lesen',
            'singing': 'Singen',
            'travelling': 'Reisen',
            'yoga': 'Yoga',
            'dancing': 'Tanzen',
            'sport': 'Sport',
            'drawing': 'Zeichnen',
            'computer_games': 'Computerspiele',
            'guitar': 'Gitarre Spielen',
            'films': 'Filme',
            'music': 'Musik',
            'knitting': 'Stricken',
            'cooking': 'Kochen',
            'fishing': 'Angeln',
            'photographing': 'Fotografieren',
        }

        res = list()

        for k in props.keys():
            if (getattr(self, k)):
                res.append(props[k])

        return res

    @property
    def get_drive_categories(self):
        props = {
            'cat_a': 'A',
            'cat_b': 'B',
            'cat_c': 'C',
            'cat_d': 'D',
            'cat_e': 'E',
            'tractor': 'Трактор',
        }

        res = list()

        for k in props.keys():
            if getattr(self, k):
                res.append(props[k])

        return res

    @property
    def get_drive_categories_wo_tractor(self):
        props = {
            'cat_a': 'A',
            'cat_b': 'B',
            'cat_c': 'C',
            'cat_d': 'D',
            'cat_e': 'E',
        }

        res = list()

        for k in props.keys():
            if getattr(self, k):
                res.append(props[k])

        return res

    @property
    def reg_address(self):
        res = [self.reg_street_number, ]
        if self.reg_city:
            res.append(self.reg_city)

        if self.reg_region:
            res.append(self.reg_region)

        res.append('Кыргызстан')

        return ', '.join(res)

    @property
    def live_address(self):
        res = [self.live_street_number, ]

        if self.live_city:
            res.append(self.live_city)

        if self.live_region:
            res.append(self.live_region)
        res.append('Кыргызстан')
        return ', '.join(res)

    @property
    def birth_place(self):
        res = []

        if self.birth_city:
            res.append(self.birth_city)

        if self.birth_region:
            res.append(self.birth_region)

        if self.birth_country:
            res.append(self.birth_country)

        return ', '.join(res)

    @property
    def reg_street_number(self):
        res = []

        if self.reg_street:
            res.append(self.reg_street)

        if self.reg_house:
            res.append(self.reg_house)

        if self.reg_apartment:
            res.append(f'/ {self.reg_apartment}')

        return ' '.join(res)

    @property
    def reg_street_number_translit(self):
        res = []

        if self.reg_street_en:
            res.append(self.reg_street_en)

        if self.reg_house:
            res.append(self.reg_house)

        if self.reg_apartment:
            res.append(f'/ {self.reg_apartment}')

        return ' '.join(res)

    @property
    def live_street_number(self):
        res = []

        if self.live_street:
            res.append(self.live_street)

        if self.live_house:
            res.append(self.live_house)

        if self.live_apartment:
            res.append(f'/ {self.live_apartment}')

        return ' '.join(res)

    @property
    def live_street_number_translit(self):
        res = []

        if self.live_street_en:
            res.append(self.live_street_en)

        if self.live_house:
            res.append(self.live_house)

        if self.live_apartment:
            res.append(f'/ {self.live_apartment}')

        return ' '.join(res)

    @staticmethod
    def get_region_en(region_ru):
        region_dict = {'Чуйская область': 'Tschui Region',
                       'Нарынская область': 'Naryn Region',
                       'Таласская область': 'Talas Region',
                       'Ыссык-Кульская область': 'Issik-Kul Region',
                       'Жалал-Абадская область': 'Zhalal-Abad Region',
                       'Ошская область': 'Osh Region',
                       'Баткенская область': 'Batken Region', }
        return region_dict.get(region_ru)

    class Meta:
        verbose_name = _('Профиль студента')
        verbose_name_plural = _('Профили студентов')

        ordering = ['last_name', 'first_name', '-creation_date']

class Contacts(Profile):
    class Meta:
        proxy = True
        verbose_name = _("Контакт студента")
        verbose_name_plural = _("Контакты студентов")


class StudentDocumentsProfileProxy(Profile):
    class Meta:
        proxy = True
        verbose_name = _("Документ Студента")
        verbose_name_plural = _("Документы Студентов")


class Interview(models.Model):
    INVITED_STATUS_CHOICES = (
        ("not_invited", _("Не оповестили")),
        ("doubtful", _("Сомнительно")),
        ("invited", _("Оповестили")),
        ("invited_twice", _("Оповестили дважды")),
    )
    profile = models.ForeignKey(Profile, verbose_name=_('Пользователь'), related_name='interviews', on_delete=models.CASCADE)
    company = models.ForeignKey(EmployerCompany, verbose_name=_('Работодатель'), related_name='interviews', on_delete=models.CASCADE, null=True)
    vacancy = ChainedForeignKey(
        Vacancy,
        verbose_name=_('Вакансия'),
        related_name='interviews',
        on_delete=models.SET_NULL,
        null=True,
        chained_field='company',
        chained_model_field='employer_company',
        show_all=False,
        auto_choose=True,
        sort=True,
    )
    city = models.CharField(_('Город'), max_length=255, blank=True)
    invited_status = models.CharField(_('Приглашен'), max_length=50, choices=INVITED_STATUS_CHOICES, default='not_invited')
    invite_date = models.DateField(_('Дата оповещения'), blank=True, null=True)
    student_confirm = models.BooleanField(_('Подтверждение студента'), default=False)
    vacancy_confirm = models.BooleanField(_('Прошел на вакансию'), default=False)
    appointment_date = models.DateTimeField(_('Дата и время собеседования'), blank=True, null=True)
    work_from = models.DateField(_('Дата начала работы'), blank=True, null=True)
    work_to = models.DateField(_('Дата окончания работы'), blank=True, null=True)

    class Meta:
        verbose_name = _('Собеседование')
        verbose_name_plural = _('Собеседования')

    def __str__(self):
        return self.profile.full_name_reverse + f'{self.appointment_date}'


def post_save_interview_profile(sender, instance, created, *args, **kwargs):
    profile = instance.profile
    last_interview = profile.interviews.filter(student_confirm=True, vacancy_confirm=True).order_by('id').last()

    if last_interview and last_interview.id == instance.id:
        profile.work_from = instance.work_from
        profile.work_to = instance.work_to
        profile.employer = instance.company
        profile.company_name = instance.company.name
        profile.position = instance.vacancy.name
        profile.save(update_fields=['work_from', 'work_to', 'company_name', 'position', 'employer', ])

    elif not last_interview:
        last_interview = profile.interviews.all().order_by('id').last()
        if last_interview and last_interview.id == instance.id:
            profile.work_from = instance.work_from
            profile.work_to = instance.work_to
            profile.save(update_fields=['work_from', 'work_to'])


post_save.connect(
    post_save_interview_profile,
    sender=Interview
)


class ProfileNotConfirmed(Profile):
    objects = ProfileNotConfirmedManager()

    class Meta:
        proxy = True
        verbose_name = _('Общий список')
        verbose_name_plural = _('Общий список')


# class ProfileInRegistration(Profile):
#     objects = ProfileInRegistrationManager()

#     class Meta:
#         proxy = True
#         verbose_name = 'На регистрации'
#         verbose_name_plural = 'На регистрации'


class ProfileInEssentialInfo(Profile):
    objects = ProfileEssentialInfoManager()

    class Meta:
        proxy = True
        verbose_name = _('Справочная информация')
        verbose_name_plural = _('Справочная информация')


# class ProfileInTermin(Profile):
#     objects = ProfileInTerminManager()

#     class Meta:
#         proxy = True
#         verbose_name = 'Термин'
#         verbose_name_plural = 'Термины'


class ProfileInInterview(Profile):
    objects = ProfileInInterviewManager()

    class Meta:
        proxy = True
        verbose_name = _('Собеседование')
        verbose_name_plural = _('Собеседование')


# class ProfileInRefused(Profile):
#     objects = ProfileRefusedManager()

#     class Meta:
#         proxy = True
#         verbose_name = 'Отказавшиеся'
#         verbose_name_plural = 'Отказавшиеся'


class ProfileInVacancy(Profile):
    objects = ProfileInVacancyManager()

    class Meta:
        proxy = True
        verbose_name = _('Вакансия')
        verbose_name_plural = _('Вакансия')
        ordering = ['termin', 'last_name', 'first_name', ]


class ProfileInEmbassy(Profile):
    objects = ProfileInEmbassyManager()

    class Meta:
        proxy = True
        verbose_name = _('Посольство')
        verbose_name_plural = _('Посольство')


# class ProfileInSending(Profile):
#     objects = ProfileInSendingManager()

#     class Meta:
#         proxy = True
#         verbose_name = 'Отправка'
#         verbose_name_plural = 'Отправка'


class ProfileInContactDetails(Profile):
    objects = ProfileInRegistrationManager()

    class Meta:
        proxy = True
        verbose_name = _('Контактные данные')
        verbose_name_plural = _('Контактные данные')


# class ProfileInArchive(Profile):
#     objects = ProfileInArchiveManager()

#     class Meta:
#         proxy = True
#         verbose_name = 'Архив'
#         verbose_name_plural = 'Архив'


class Bill(models.Model):
    profile = models.ForeignKey(Profile, verbose_name=_('Оплатил'), related_name='bills', on_delete=models.PROTECT)
    who_created = models.ForeignKey(User, verbose_name=_('Оплату принял'), related_name='bills', on_delete=models.PROTECT)
    pay_sum = models.IntegerField(_('Сумма оплаты'))
    created_at = models.DateTimeField(_('Время создания счета'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Время изменения счета'), auto_now=True)

    class Meta:
        verbose_name = _('Счет')
        verbose_name_plural = _('Счета')

    def __str__(self):
        return f'{self.id}'


class ProfileHistory(models.Model):

    username = models.CharField(verbose_name=_('Автор изменений'), max_length=128)
    date = models.DateTimeField(verbose_name=_('Дата изменений'), blank=True, null=True)
    changes = RichTextField(verbose_name=_('Текст изменения'))

    def __str__(self):
        return self.username + "' changes"

    class Meta:
        verbose_name = _('История изменений Характеристики')
        verbose_name_plural = _('Истории изменений Характеристики')



@receiver(post_save, sender=Profile)
def count_amount_of_profiles(sender, instance, created, **kwargs):

    if created:
        history, created = ProfileCounter.objects.get_or_create(creation_date=datetime.date.today())
        
        names = history.list_of_names

        if names is not None:

            if hasattr(instance, 'full_name'):
                history.list_of_names.append(instance.full_name)
                
            else:
                history.list_of_names.append(instance.user.email)
        else:
            names = []
            if hasattr(instance, 'full_name'):
                names.append(instance.full_name)

            else:
                names.append(instance.user.email)
            history.list_of_names = names

        history.amount_of_profiles += 1
        history.save(update_fields=['list_of_names', 'amount_of_profiles'])


class SupportRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    message = RichTextField(_('Сообщение'))
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
   

    

    def str(self):
        return f"Запрос от {self.user.email}: {self.created_at}"
    
    class Meta:
        verbose_name = _('Тех поддержка')
        verbose_name_plural = _('Тех поддержка')
    

class SupportResponse(models.Model):
    support_request = models.ForeignKey(SupportRequest, on_delete=models.CASCADE, related_name='response')
    message = RichTextField(_('Ответ'))
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    sent = models.BooleanField(_('Отправлено'), default=False)
    
    def save(self, *args, **kwargs):
        self.sent = True
        super(SupportResponse, self).save(*args, **kwargs)
    

    def str(self):
        return f"Ответ к запросу {self.support_request.id}"


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True)
    photo = models.ImageField(upload_to="announcements/", blank=True, null=True)
    video = models.FileField(upload_to="announcement_videos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    specific_student = models.ForeignKey(
        User,
        related_name="student_announcements",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    specific_employer = models.ForeignKey(
        User,
        related_name="employer_announcements",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    send_to_students = models.BooleanField(
        default=False, verbose_name=_("Отправить студентам")
    )
    send_to_employers = models.BooleanField(
        default=False, verbose_name=_("Отправить работодателям")
    )

    class Meta:
        verbose_name = _("Объявление")
        verbose_name_plural = _("Объявления")

    def str(self):
        return self.title
    
class ConnectionRequest(models.Model):
    full_name = models.CharField(_("ФИО"), max_length=255, blank=True, null=True)
    email = models.EmailField(_("Емайл"), unique=True)
    phone = models.CharField(_("Номер телефона"), max_length=50)
    request_date = models.DateTimeField(_("Дата заявки"), default=timezone.now)
    manager_notes = RichTextField(_("Примечание менеджера"), blank=True, null=True)
    call_date = models.DateField(_("Дата звонка менеджера"), blank=True, null=True)
    text = RichTextField(_("Комментарий"), blank=True, null=True)
    called = models.BooleanField(_("Позвонил"), default=False)
    consulted = models.BooleanField(_("Проконсультирован"), default=False)
    call_later = models.BooleanField(_("Набрать позже"), default=False)
    paid = models.BooleanField(_("Оплачен"), default=False)
    

    def str(self):
        return self.email

    class Meta:
        verbose_name = _("Заявка на подключение")
        verbose_name_plural = _("Заявки на подключение")