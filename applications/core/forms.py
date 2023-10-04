import re
import datetime

from PIL import Image as PilImage

from django import forms

from applications.accounts.models import Profile


TRUE_FALSE_CHOICES = (
    (True, 'Есть'),
    (False, 'Нет'),
)

CHOICES = (
    (True, 'Да'),
    (False, 'Нет'),
)


class CustomCharField(forms.CharField):
    def validate(self, value):
        pass


class MainQuestionnaireForm(forms.ModelForm):
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'id': 'phone',
                'class': 'input-wrapper__input',
                'readonly': 'readonly',
            }
        )
    )
    whatsapp_phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'id': 'whatsapp_phone',
                'class': 'input-wrapper__input',
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'email',
                'class': 'input-wrapper__input',
                'readonly': 'readonly',
            }
        )
    )
    university = CustomCharField(
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'id': 'university',
                'class': 'input-wrapper__input',
                'readonly': 'readonly',
            }
        )
    )
    faculty = CustomCharField(
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'id': 'faculty',
                'class': 'input-wrapper__input',
                'readonly': 'readonly',
            }
        )
    )
    study_start = CustomCharField(
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'id': 'study_start',
                'class': 'input-wrapper__input',
            }
        )
    )
    study_end = CustomCharField(
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'id': 'study_end',
                'class': 'input-wrapper__input',
            }
        )
    )
    rotate = forms.IntegerField(required=False)
    bday = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'text',
                'id': 'bday',
                'class': 'input-wrapper__input',
                'readonly': 'readonly',
            },
            format='%d-%m-%Y',
        ),
        input_formats=[
            '%d-%m-%Y',
            '%d.%m.%Y',
            '%d/%m/%Y',
        ],
        error_messages={
            'invalid': 'Формат даты рождения неверный.',
        }
    )

    zagranpassport_end_time = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'text',
                'data-type': 'date',
                'id': 'zagranpassport_end_time',
                'class': 'input-wrapper__input',
            },
            format='%d-%m-%Y',
        ),
        input_formats=[
            '%d-%m-%Y',
            '%d.%m.%Y',
            '%d/%m/%Y',
        ],
        error_messages={
            'invalid': 'Формат даты окончания паспорта неверный.',
        },
        required=False,
    )

    start_date1 = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'data-type': 'date',
                'id': 'start_date1',
                'class': 'input-wrapper__input',
            },
            format='%d-%m-%Y',
        ),
        input_formats=[
            '%d-%m-%Y',
            '%d.%m.%Y',
            '%d/%m/%Y',
        ],
        error_messages={
            'invalid': 'Формат даты неверный.',
        }
    )
    end_date1 = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'data-type': 'date',
                'id': 'end_date1',
                'class': 'input-wrapper__input',
            },
            format='%d-%m-%Y',
        ),
        input_formats=[
            '%d-%m-%Y',
            '%d.%m.%Y',
            '%d/%m/%Y',
        ],
        error_messages={
            'invalid': 'Формат даты неверный.',
        }
    )
    start_date2 = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'data-type': 'date',
                'id': 'start_date2',
                'class': 'input-wrapper__input',
            },
            format='%d-%m-%Y',
        ),
        input_formats=[
            '%d-%m-%Y',
            '%d.%m.%Y',
            '%d/%m/%Y',
        ],
        error_messages={
            'invalid': 'Формат даты неверный.',
        }
    )
    end_date2 = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'data-type': 'date',
                'id': 'end_date2',
                'class': 'input-wrapper__input',
            },
            format='%d-%m-%Y',
        ),
        input_formats=[
            '%d-%m-%Y',
            '%d.%m.%Y',
            '%d/%m/%Y',
        ],
        error_messages={
            'invalid': 'Формат даты неверный.',
        }
    )
    start_date3 = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'data-type': 'date',
                'id': 'start_date3',
                'class': 'input-wrapper__input',
            },
            format='%d-%m-%Y',
        ),
        input_formats=[
            '%d-%m-%Y',
            '%d.%m.%Y',
            '%d/%m/%Y',
        ],
        error_messages={
            'invalid': 'Формат даты неверный.',
        },
        required=False,
    )
    end_date3 = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'data-type': 'date',
                'id': 'end_date3',
                'class': 'input-wrapper__input',
            },
            format='%d-%m-%Y',
        ),
        input_formats=[
            '%d-%m-%Y',
            '%d.%m.%Y',
            '%d/%m/%Y',
        ],
        error_messages={
            'invalid': 'Формат даты неверный.',
        },
        required=False,
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'gender', 'bday', 'nationality', 'been_to_germany', 'birth_country', 'birth_region',
                  'birth_city', 'reg_region', 'reg_city', 'reg_district', 'reg_street', 'reg_house', 'reg_apartment',
                  'live_region', 'live_city', 'live_district', 'live_street', 'live_house', 'live_apartment', 
                  'passport_number', 'zagranpassport_number', 'zagranpassport_end_time', 'university', 'faculty', 'degree', 'year', 'study_start',
                  'study_end', 'father_phone', 'father_work_phone', 'father_company', 'mother_phone', 'mother_work_phone',
                  'mother_company', 'company1', 'position1', 'start_date1', 'end_date1', 'country1', 'company2',
                  'position2', 'start_date2', 'end_date2', 'country2', 'company3', 'position3', 'start_date3', 'end_date3',
                  'country3', 'german', 'english', 'turkish', 'russian', 'chinese', 'driver_license', 'driving_experience',
                  'cat_a', 'cat_b', 'cat_c', 'cat_d', 'cat_e', 'tractor', 'transmission', 'shirt_size', 'pants_size',
                  'shoe_size', 'reading', 'singing', 'travelling', 'yoga', 'dancing', 'sport', 'drawing', 'computer_games',
                  'guitar', 'films', 'music', 'knitting', 'cooking', 'fishing', 'photographing', 'phone', 'whatsapp_phone',
                  'email', 'rotate', 'first_name_ru', 'last_name_ru', 'bicycle_skill', 'reg_city_en', 'reg_district_en',
                  'reg_street_en', 'live_city_en', 'live_district_en', 'live_street_en']

        required = ['first_name', 'last_name', 'gender', 'bday', 'nationality', 'birth_country', 'reg_region', 'reg_city',
                    'reg_district', 'reg_street', 'reg_house', 'live_region', 'live_city', 'live_district', 'live_street',
                    'live_house', 'passport_number', 'zagranpassport_number', 'phone', 'whatsapp_phone', 'email',
                    'university', 'faculty', 'degree', 'year', 'study_start', 'study_end', 'father_phone', 'father_company',
                    'mother_phone', 'mother_company', 'company1', 'position1', 'start_date1', 'end_date1', 'country1',
                    'company2', 'position2', 'start_date2', 'end_date2', 'country2', 'german', 'english', 'turkish',
                    'russian', 'chinese', 'shirt_size', 'pants_size', 'shoe_size', 'first_name_ru', 'last_name_ru',
                    'bicycle_skill', 'reg_city_en', 'reg_district_en', 'reg_street_en', 'live_city_en', 'live_district_en',
                    'live_street_en']

        widgets = {
            'first_name': forms.TextInput(attrs={'type': 'text', 'id':'first_name', 'class': 'input-wrapper__input', 'readonly': 'readonly'}),
            'last_name': forms.TextInput(attrs={'type': 'text', 'id': 'last_name', 'class': 'input-wrapper__input', 'readonly': 'readonly'}),
            'first_name_ru': forms.TextInput(attrs={'type': 'text', 'id': 'first_name_ru', 'class': 'input-wrapper__input'}),
            'last_name_ru': forms.TextInput(attrs={'type': 'text', 'id': 'last_name_ru', 'class': 'input-wrapper__input'}),
            # 'bday': forms.DateInput(attrs={'type': 'text', 'data-type': 'date', 'id': 'bday', 'class': 'input-wrapper__input', 'readonly': 'readonly'}, format='%d-%m-%Y'),
            'gender': forms.Select(attrs={'id': 'gender', 'class': 'select-wrapper__select'}),
            'nationality': forms.Select(attrs={'id': 'nationality', 'class': 'select-wrapper__select'}),
            'birth_country': forms.Select(attrs={'id': 'birth_country', 'class': 'select-wrapper__select'}),
            'birth_region': forms.Select(attrs={'id': 'birth_region', 'class': 'select-wrapper__select'}),
            'birth_city': forms.TextInput(attrs={'type': 'text', 'id': 'birth_city', 'class': 'input-wrapper__input'}),
            'reg_region': forms.Select(attrs={'id': 'reg_region', 'class': 'select-wrapper__select'}),
            'reg_city': forms.TextInput(attrs={'type': 'text', 'id': 'reg_city', 'class': 'input-wrapper__input'}),
            'reg_city_en': forms.TextInput(attrs={'type': 'text', 'id': 'reg_city_en', 'class': 'input-wrapper__input'}),
            'reg_district': forms.TextInput(attrs={'type': 'text', 'id': 'reg_district', 'class': 'input-wrapper__input'}),
            'reg_district_en': forms.TextInput(attrs={'type': 'text', 'id': 'reg_district_en', 'class': 'input-wrapper__input'}),
            'reg_street': forms.TextInput(attrs={'type': 'text', 'id': 'reg_street', 'class': 'input-wrapper__input'}),
            'reg_street_en': forms.TextInput(attrs={'type': 'text', 'id': 'reg_street_en', 'class': 'input-wrapper__input'}),
            'reg_house': forms.TextInput(attrs={'type': 'text', 'id': 'reg_house', 'class': 'input-wrapper__input'}),
            'reg_apartment': forms.TextInput(attrs={'type': 'text', 'id': 'reg_apartment', 'class': 'input-wrapper__input'}),
            'live_region': forms.Select(attrs={'id': 'live_region', 'class': 'select-wrapper__select'}),
            'live_city': forms.TextInput(attrs={'type': 'text', 'id': 'live_city', 'class': 'input-wrapper__input'}),
            'live_city_en': forms.TextInput(attrs={'type': 'text', 'id': 'live_city_en', 'class': 'input-wrapper__input'}),
            'live_district': forms.TextInput(attrs={'type': 'text', 'id': 'live_district', 'class': 'input-wrapper__input'}),
            'live_district_en': forms.TextInput(attrs={'type': 'text', 'id': 'live_district_en', 'class': 'input-wrapper__input'}),
            'live_street': forms.TextInput(attrs={'type': 'text', 'id': 'live_street', 'class': 'input-wrapper__input'}),
            'live_street_en': forms.TextInput(attrs={'type': 'text', 'id': 'live_street_en', 'class': 'input-wrapper__input'}),
            'live_house': forms.TextInput(attrs={'type': 'text', 'id': 'live_house', 'class': 'input-wrapper__input'}),
            'live_apartment': forms.TextInput(attrs={'type': 'text', 'id': 'live_apartment', 'class': 'input-wrapper__input'}),
            'been_to_germany': forms.Select(attrs={'id': 'been_to_germany', 'class': 'select-wrapper__select'}, choices=CHOICES),
            'passport_number': forms.TextInput(attrs={'type': 'text', 'id': 'passport_number', 'class': 'input-wrapper__input'}),
            'zagranpassport_number': forms.TextInput(attrs={'type': 'text', 'id': 'zagranpassport_number', 'class': 'input-wrapper__input'}),
            # 'zagranpassport_end_time': forms.TextInput(attrs={'type': 'text', 'data-type': 'date', 'id': 'zagranpassport_end_time', 'class': 'input-wrapper__input'}),
            # 'university': forms.TextInput(attrs={'type': 'text', 'id': 'university', 'class': 'input-wrapper__input', 'readonly': 'readonly'}),
            # 'faculty': forms.TextInput(attrs={'type': 'text', 'id': 'faculty', 'class': 'input-wrapper__input', 'readonly': 'readonly'}),
            'degree': forms.Select(attrs={'id': 'degree', 'class': 'select-wrapper__select'}),
            'year': forms.Select(attrs={'id': 'year', 'class':'select-wrapper__select'}),
            # 'study_start': forms.TextInput(attrs={'type': 'text', 'id': 'study_start', 'class': 'input-wrapper__input'}),
            # 'study_end': forms.TextInput(attrs={'type': 'text', 'id': 'study_end', 'class': 'input-wrapper__input'}),
            'father_phone': forms.TextInput(attrs={'type': 'text', 'id': 'father_phone', 'class': 'input-wrapper__input'}),
            'father_work_phone': forms.TextInput(attrs={'type': 'text', 'id': 'father_work_phone', 'class': 'input-wrapper__input'}),
            'father_company': forms.TextInput(attrs={'type': 'text', 'id': 'father_company', 'class': 'input-wrapper__input'}),
            'mother_phone': forms.TextInput(attrs={'type': 'text', 'id': 'mother_phone', 'class': 'input-wrapper__input'}),
            'mother_work_phone': forms.TextInput(attrs={'type': 'text', 'id': 'mother_work_phone', 'class': 'input-wrapper__input'}),
            'mother_company': forms.TextInput(attrs={'type': 'text', 'id': 'mother_company', 'class': 'input-wrapper__input'}),
            'company1': forms.TextInput(attrs={'type': 'text', 'id': 'company1', 'class': 'input-wrapper__input'}),
            'position1': forms.Select(attrs={'id': 'position1', 'class': 'select-wrapper__select'}),
            # 'start_date1': forms.DateInput(attrs={'data-type': 'date', 'id': 'start_date1', 'class': 'input-wrapper__input'}, format='%d-%m-%Y'),
            # 'end_date1': forms.DateInput(attrs={'data-type': 'date', 'id': 'end_date1', 'class': 'input-wrapper__input'}, format='%d-%m-%Y'),
            'country1': forms.Select(attrs={'id': 'country1', 'class': 'select-wrapper__select'}),
            'company2': forms.TextInput(attrs={'type': 'text', 'id': 'company2', 'class': 'input-wrapper__input'}),
            'position2': forms.Select(attrs={'id': 'position2', 'class': 'select-wrapper__select'}),
            # 'start_date2': forms.DateInput(attrs={'data-type': 'date', 'id': 'start_date2', 'class': 'input-wrapper__input'}, format='%d-%m-%Y'),
            # 'end_date2': forms.DateInput(attrs={'data-type': 'date', 'id': 'end_date2', 'class': 'input-wrapper__input'}, format='%d-%m-%Y'),
            'country2': forms.Select(attrs={'id': 'country2', 'class': 'select-wrapper__select'}),
            'company3': forms.TextInput(attrs={'type': 'text', 'id': 'company3', 'class': 'input-wrapper__input'}),
            'position3': forms.Select(attrs={'id': 'position3', 'class': 'select-wrapper__select'}),
            # 'start_date3': forms.DateInput(attrs={'data-type': 'date', 'id': 'start_date3', 'class': 'input-wrapper__input'}, format='%d-%m-%Y'),
            # 'end_date3': forms.DateInput(attrs={'data-type': 'date', 'id': 'end_date3', 'class': 'input-wrapper__input'}, format='%d-%m-%Y'),
            'country3': forms.Select(attrs={'id': 'country3', 'class': 'select-wrapper__select'}),
            'german': forms.Select(attrs={'id': 'german', 'class': 'select-wrapper__select'}),
            'english': forms.Select(attrs={'id': 'english', 'class': 'select-wrapper__select'}),
            'turkish': forms.Select(attrs={'id': 'turkish', 'class': 'select-wrapper__select'}),
            'russian': forms.Select(attrs={'id': 'russian', 'class': 'select-wrapper__select'}),
            'chinese': forms.Select(attrs={'id': 'chinese', 'class': 'select-wrapper__select'}),
            'driver_license': forms.Select(attrs={'id': 'driver_license', 'class': 'select-wrapper__select'}, choices=TRUE_FALSE_CHOICES),
            'bicycle_skill': forms.Select(attrs={'id': 'bicycle_skill', 'class': 'select-wrapper__select'}),
            'cat_a': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'cat_a', 'class': 'checkbox-wrapper__check'}),
            'cat_b': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'cat_b', 'class': 'checkbox-wrapper__check'}),
            'cat_c': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'cat_c', 'class': 'checkbox-wrapper__check'}),
            'cat_d': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'cat_d', 'class': 'checkbox-wrapper__check'}),
            'cat_e': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'cat_e', 'class': 'checkbox-wrapper__check'}),
            'tractor': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'tractor', 'class': 'checkbox-wrapper__check'}),
            'driving_experience': forms.Select(attrs={'id': 'driving_experience', 'class': 'select-wrapper__select'}),
            'transmission': forms.Select(attrs={'id': 'transmission', 'class': 'select-wrapper__select'}),
            'reading': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'reading', 'class': 'checkbox-wrapper__check'}),
            'singing': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'singing', 'class': 'checkbox-wrapper__check'}),
            'travelling': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'travelling', 'class': 'checkbox-wrapper__check'}),
            'yoga': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'yoga', 'class': 'checkbox-wrapper__check'}),
            'dancing': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'dancing', 'class': 'checkbox-wrapper__check'}),
            'sport': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'sport', 'class': 'checkbox-wrapper__check'}),
            'drawing': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'drawing', 'class': 'checkbox-wrapper__check'}),
            'computer_games': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'computer_games', 'class': 'checkbox-wrapper__check'}),
            'guitar': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'guitar', 'class': 'checkbox-wrapper__check'}),
            'films': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'films', 'class': 'checkbox-wrapper__check'}),
            'music': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'music', 'class': 'checkbox-wrapper__check'}),
            'knitting': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'knitting', 'class': 'checkbox-wrapper__check'}),
            'cooking': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'cooking', 'class': 'checkbox-wrapper__check'}),
            'fishing': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'fishing', 'class': 'checkbox-wrapper__check'}),
            'photographing': forms.CheckboxInput(attrs={'type': 'checkbox', 'id': 'photographing', 'class': 'checkbox-wrapper__check'}),
            'shirt_size': forms.Select(attrs={'id': 'shirt_size', 'class': 'select-wrapper__select'}),
            'pants_size': forms.Select(attrs={'id': 'pants_size', 'class': 'select-wrapper__select'}),
            'shoe_size': forms.Select(attrs={'id': 'shoe_size', 'class': 'select-wrapper__select'}),
        }

        labels = {
            'first_name': 'Имя (Личные данные)',
            'last_name': 'Фамилия (Личные данные)',
            'first_name_ru': 'Имя на русском (Личные данные)',
            'last_name_ru': 'Фамилия на русском (Личные данные)',
            'gender': 'Пол (Личные данные)',
            'bday': 'Дата рождения (Личные данные)',
            'nationality': 'Гражданство (Личные данные)',
            'been_to_germany': 'Был в Германии',
            'birth_country': 'Страна (Место рождения)',
            'birth_region': 'Область (Место рождения)',
            'birth_city': 'Город/село (Место рождения)',
            'reg_region': 'Область (Адрес прописки)',
            'reg_city': 'Город на русском (Адрес прописки)',
            'reg_city_en': 'Город на латинице (Адрес прописки)',
            'reg_district': 'Район на русском (Адрес прописки)',
            'reg_district_en': 'Район на латинице (Адрес прописки)',
            'reg_street': 'Улица или микрорайон на русском (Адрес прописки)',
            'reg_street_en': 'Улица или микрорайон на латинице (Адрес прописки)',
            'reg_house': 'Дом (Адрес прописки)',
            'reg_apartment': 'Квартира (Адрес прописки)',
            'live_region': 'Область (Фактический адрес)',
            'live_city': 'Город на русском (Фактический адрес)',
            'live_city_en': 'Город на латинице (Фактический адрес)',
            'live_district': 'Район на русском (Фактический адрес)',
            'live_district_en': 'Район на латинице (Фактический адрес)',
            'live_street': 'Улица или микрорайон на русском (Фактический адрес)',
            'live_street_en': 'Улица или микрорайон на латинице (Фактический адрес)',
            'live_house': 'Дом (Фактический адрес)',
            'live_apartment': 'Квартира (Фактический адрес)',
            'passport_number': 'Номер ID паспорта (Паспортные данные)',
            'zagranpassport_number': 'Номер загранпаспорта (Паспортные данные)',
            'zagranpassport_end_time': 'Время окончания загранпаспорта (Паспортные данные)',
            'phone': 'Номер телефона (Контакты)',
            'whatsapp_phone': 'Номер What\'s App (Контакты)',
            'email': 'Email (Контакты)',
            'university': 'Университет (Информация об университете)',
            'faculty': 'Факультет или направление (Информация об университете)',
            'degree': 'Академическая степень (Информация об университете)',
            'year': 'Курс (Информация об университете)',
            'study_start': 'Дата начала (Информация об университете)',
            'study_end': 'Дата окончания (Информация об университете)',
            'father_phone': 'Контактный номер отца (Информация о родителях)',
            'father_work_phone': 'Рабочий номер отца (Информация о родителях)',
            'father_company': 'Место работы отца (Информация о родителях)',
            'mother_phone': 'Контактный номер матери (Информация о родителях)',
            'mother_work_phone': 'Рабочий номер матери (Информация о родителях)',
            'mother_company': 'Место работы матери (Информация о родителях)',
            'company1': 'Компания (1 место работы)',
            'position1': 'Должность (1 место работы)',
            'start_date1': 'Период работы от (1 место работы)',
            'end_date1': 'Период работы до (1 место работы)',
            'country1': 'Страна (1 место работы)',
            'company2': 'Компания (2 место работы)',
            'position2': 'Должность (2 место работы)',
            'start_date2': 'Период работы от (2 место работы)',
            'end_date2': 'Период работы до (2 место работы)',
            'country2': 'Страна (2 место работы)',
            'company3': 'Компания (3 место работы)',
            'position3': 'Должность (3 место работы)',
            'start_date3': 'Период работы от (3 место работы)',
            'end_date3': 'Период работы до (3 место работы)',
            'country3': 'Страна (3 место работы)',
            'german': 'Немецкий язык (Владение языками)',
            'english': 'Английский язык (Владение языками)',
            'turkish': 'Турецкий язык (Владение языками)',
            'russian': 'Русский язык (Владение языками)',
            'chinese': 'Китайский язык (Владение языками)',
            'driver_license': 'Водительские права (Водительские права)',
            'driving_experience': 'Стаж вождения (Водительские права)',
            'cat_a': 'Категория A (Водительские права)',
            'cat_b': 'Категория B (Водительские права)',
            'cat_c': 'Категория C (Водительские права)',
            'cat_d': 'Категория D (Водительские права)',
            'cat_e': 'Категория E (Водительские права)',
            'tractor': 'Категория трактор (Водительские права)',
            'transmission': 'Механика или автомат (Водительские права)',
            'bicycle_skill': 'Умеете ли ездить на велосипеде',
            'shirt_size': 'Размер рубашки (Дополнительная информация)',
            'pants_size': 'Размер брюк (Дополнительная информация)',
            'shoe_size': 'Размер обуви (Дополнительная информация)',
            'reading': 'Хобби',
            'singing': 'Пение (Хобби)',
            'travelling': 'Путешествия (Хобби)',
            'yoga': 'Йога (Хобби)',
            'dancing': 'Танцы (Хобби)',
            'sport': 'Спорт (Хобби)',
            'drawing': 'Рисование (Хобби)',
            'computer_games': 'Компьютерные игры (Хобби)',
            'guitar': 'Игра на гитаре (Хобби)',
            'films': 'Фильмы (Хобби)',
            'music': 'Музыка (Хобби)',
            'knitting': 'Вязание (Хобби)',
            'cooking': 'Готовка (Хобби)',
            'fishing': 'Рыбалка (Хобби)',
            'photographing': 'Фотография (Хобби)',
        }

    def __init__(self, *args, **kwargs):
        super(MainQuestionnaireForm, self).__init__(*args, **kwargs)
        self.fields['gender'].choices = [('', ''), ] + list(self.fields['gender'].choices)[1:]
        self.fields['nationality'].choices = [('', ''), ] + list(self.fields['nationality'].choices)[1:]
        self.fields['birth_country'].choices = [('', ''), ] + list(self.fields['birth_country'].choices)[1:]
        self.fields['birth_region'].choices = [('', ''), ] + list(self.fields['birth_region'].choices)[1:]
        self.fields['reg_region'].choices = [('', ''), ] + list(self.fields['reg_region'].choices)[1:]
        self.fields['live_region'].choices = [('', ''), ] + list(self.fields['live_region'].choices)[1:]
        self.fields['degree'].choices = [('', ''), ] + list(self.fields['degree'].choices)[1:]
        self.fields['year'].choices = [('', ''), ] + list(self.fields['year'].choices)[1:]
        self.fields['position1'].choices = [('', ''), ] + list(self.fields['position1'].choices)[1:]
        self.fields['country1'].choices = [('', ''), ] + list(self.fields['country1'].choices)[1:]
        self.fields['position2'].choices = [('', ''), ] + list(self.fields['position2'].choices)[1:]
        self.fields['country2'].choices = [('', ''), ] + list(self.fields['country2'].choices)[1:]
        self.fields['position3'].choices = [('', ''), ] + list(self.fields['position3'].choices)[1:]
        self.fields['country3'].choices = [('', ''), ] + list(self.fields['country3'].choices)[1:]
        self.fields['german'].choices = [('', ''), ] + list(self.fields['german'].choices)[1:]
        self.fields['english'].choices = [('', ''), ] + list(self.fields['english'].choices)[1:]
        self.fields['turkish'].choices = [('', ''), ] + list(self.fields['turkish'].choices)[1:]
        self.fields['russian'].choices = [('', ''), ] + list(self.fields['russian'].choices)[1:]
        self.fields['chinese'].choices = [('', ''), ] + list(self.fields['chinese'].choices)[1:]
        self.fields['driving_experience'].choices = [('', ''), ] + list(self.fields['driving_experience'].choices)[1:]
        self.fields['transmission'].choices = [('', ''), ] + list(self.fields['transmission'].choices)[1:]
        self.fields['shirt_size'].choices = [('', ''), ] + list(self.fields['shirt_size'].choices)[1:]
        self.fields['pants_size'].choices = [('', ''), ] + list(self.fields['pants_size'].choices)[1:]
        self.fields['shoe_size'].choices = [('', ''), ] + list(self.fields['shoe_size'].choices)[1:]
        self.fields['bicycle_skill'].choices = [('', ''), ] + list(self.fields['bicycle_skill'].choices)[1:]
        self.fields['rotate'].label = 'Фотография'

        for field in self.Meta.required:
            self.fields[field].required = True
            self.fields[field].error_messages = {
                'required': 'Поле обязательно для заполнения.',
            }

    def clean_study_start(self):
        study_start = self.cleaned_data.get('study_start')
        if study_start and study_start.isdigit() and study_start.startswith('20') and len(study_start) == 4:
            return f'{study_start}-09-01'
        raise forms.ValidationError('Укажите правильную дату поступления.')

    def clean_university(self):
        return None

    def clean_faculty(self):
        return None

    def clean_study_end(self):
        study_end = self.cleaned_data.get('study_end')
        if study_end and study_end.isdigit() and study_end.startswith('20') and len(study_end) == 4:
            return f'{study_end}-06-30'
        raise forms.ValidationError('Укажите правильную дату окончания')

    def clean_rotate(self):
        if not self.instance.photo:
            raise forms.ValidationError('Поле обязательно для заполнения.')
        rotate_angle = self.cleaned_data.get('rotate')
        if rotate_angle and rotate_angle != 0:
            im = PilImage.open(self.instance.photo)
            rotated_image = im.rotate(-rotate_angle)
            rotated_image.save(self.instance.photo.file.name, overwrite=True)

    def clean_driving_experience(self):
        if self.cleaned_data.get('driver_license') and not self.cleaned_data.get('driving_experience'):
            raise forms.ValidationError('Укажите стаж вождения')

        return self.cleaned_data.get('driving_experience')

    def clean_transmission(self):
        if self.cleaned_data.get('driver_license') and not self.cleaned_data.get('transmission'):
            raise forms.ValidationError('Укажите тип КПП')

        return self.cleaned_data.get('transmission')

    def clean_first_name_ru(self):
        first_name_ru = self.cleaned_data.get('first_name_ru', '').strip()
        return first_name_ru

    def clean_last_name_ru(self):
        last_name_ru = self.cleaned_data.get('last_name_ru', '').strip()
        return last_name_ru

    # TODO: add checks for kirill and - , : in the following fields
    # reg_region reg_city reg_district reg_street reg_house reg_apartment live_region live_city
    # live_district live_street live_house live_apartment first_name_ru last_name_ru
    
    def sort_work_experience(self, data_list, obj):

        data_list = [i for i in data_list if i['start_date'] != None]
        data_list = sorted(data_list, key=lambda k: k['start_date'], reverse=True)

        for i in range (1, len(data_list)+1):
            obj[f'start_date{i}'] = data_list[i-1]['start_date']
            obj[f'company{i}'] = data_list[i-1]['company']
            obj[f'country{i}'] = data_list[i-1]['country']
            obj[f'position{i}'] = data_list[i-1]['position']
            obj[f'end_date{i}'] = data_list[i-1]['end_date']

        return obj
    
    def generate_list(self, obj):

        data_list = []
        for i in range (1, 4):
            
            data_dict = {}
            data_dict['start_date'] = obj.get(f'start_date{i}')
            data_dict['company'] = obj.get(f'company{i}')
            data_dict['country'] = obj.get(f'country{i}')
            data_dict['position'] = obj.get(f'position{i}')
            data_dict['end_date'] = obj.get(f'end_date{i}')

            data_list.append(data_dict)

        return data_list

    def clean(self):
        cleaned_data = super(MainQuestionnaireForm, self).clean()

        # check whether at least 1 driving category selected
        driver_categories = ['cat_a', 'cat_b', 'cat_c', 'cat_d', 'cat_e', 'tractor', ]
        driver_categories_data = [cleaned_data.get(key) for key in driver_categories]
        if cleaned_data.get('driver_license') and not any(driver_categories_data):
            self.add_error('driver_license', 'Укажите хотя бы одну категорию прав.')

        # check whether at least 1 hobby selected
        hobbies_fields = ['reading', 'singing', 'travelling', 'yoga', 'dancing', 'sport', 'drawing', 'computer_games',
                          'guitar', 'films', 'music', 'knitting', 'cooking', 'fishing', 'photographing',]
        hobbies_data = [cleaned_data.get(key) for key in hobbies_fields]
        if not any(hobbies_data):
            self.add_error('reading', 'Укажите хотя бы одно хобби.')
        

        for i in ['date1', 'date2', 'date3']:
            if self.cleaned_data.get(f'start_{i}') and self.cleaned_data.get(f'end_{i}'):

                if self.cleaned_data.get(f'start_{i}') > self.cleaned_data.get(f'end_{i}'):

                    self.add_error(f'start_{i}', 'Дата начала не должна быть позже даты конца опыта')

        companies = ['company1', 'company2', ]

        if self.cleaned_data.get('company3'):

            companies.append('company3')

        for company in companies:

            if self.cleaned_data.get(company):

                if not re.match("[a-zA-Z0-9\s]", self.cleaned_data.get(company)):
                    self.add_error(company, f'Используйте латиницу для поля {self.Meta.labels[company]}')

        # sort work experience by date(from earliest to latest)
        data_list = self.generate_list(cleaned_data)
        cleaned_data = self.sort_work_experience(data_list, cleaned_data)

        return cleaned_data


    def save(self, commit=True):
        readonly_fields = ['first_name', 'last_name', 'bday', 'university', 'faculty', 'whatsapp_phone', 'email', 'phone', 'rotate']
        [setattr(self.instance, key, value) for (key, value) in self.cleaned_data.items() if key not in readonly_fields]
        self.instance.save(update_fields=[key for key in self.cleaned_data.keys() if key not in readonly_fields])

        user = self.instance.user
        user.whatsapp_phone = self.cleaned_data.get('whatsapp_phone')
        user.save(update_fields=['whatsapp_phone', ])

        self.instance.is_form_completed = True
        self.instance.save(update_fields=['is_form_completed'])

        return user, self.instance


class FileUploadForm(forms.Form):
    photo = forms.ImageField()

    def __init__(self, *args, **kwargs):
        self._profile = kwargs.pop('profile')
        super().__init__(*args, **kwargs)

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if not photo:
            raise forms.ValidationError('Фотография не загружена!')
        return photo

    def save(self):
        self._profile.photo = self.cleaned_data.get('photo')
        self._profile.save()
        return self._profile


class DocumentUploadForm(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        self._profile = kwargs.pop('profile')
        super().__init__(*args, **kwargs)

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise forms.ValidationError('Файл не загружен!')
        return file

    def save(self, file_label):
        setattr(self._profile, file_label, self.cleaned_data.get('file'))
        self._profile.save(update_fields=[file_label])
        return self._profile
