from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.forms.widgets import ChoiceWidget
from django.template import loader
from django.utils.safestring import mark_safe

from applications.accounts.models import Profile, Staff
from applications.accounts.utils import only_roman_chars
from applications.core.models import University, Faculty, ContractAdmin, Tariff
from applications.core.constants import (
    DOCUMENT_TYPE_CHOICES,
    EMPLOYMENT_DOCUMENT_TYPE_CHOICES,
    AGREEMENT_ACT_TYPE_CHOICES,
    CLOSURE_DOC_TYPE_CHOICES,
)

User = get_user_model()



class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'email',
                'class': 'input-wrapper__input',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'password',
                'class': 'input-wrapper__input',
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        return email

    def clean(self):
        user = authenticate(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))
        if user:
            return self.cleaned_data
        raise forms.ValidationError('Неверный email или пароль.')


class EmploymentDocumentsForm(forms.Form):
    employment_document_type = forms.CharField(
        widget=forms.Select(
            attrs={'class': 'form-control'},
            choices=EMPLOYMENT_DOCUMENT_TYPE_CHOICES
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('employment_document_type') not in ['1000', '2000']:
            self.add_error('employment_document_type', 'Выберите тип договора из списка.')
        return cleaned_data


class RegistrationForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'email',
                'class': 'input-wrapper__input',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'password',
                'class': 'input-wrapper__input',
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'password2',
                'class': 'input-wrapper__input',
            }
        )
    )
    birthday = forms.DateField(
        input_formats=[
            '%d-%m-%Y',
        ],
        error_messages={
            'invalid': 'Формат даты рождения неверный.'
        }
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'firstname',
                'class': 'input-wrapper__input',
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'lastname',
                'class': 'input-wrapper__input',
            }
        )
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'phone',
                'class': 'input-wrapper__input',
            }
        )
    )
    university = forms.IntegerField()
    faculty = forms.IntegerField()

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        qs = User.objects.filter(email=email)
        if qs.exists() and qs.count() == 1:
            raise forms.ValidationError('Указанный email адрес занят.')
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Пароли не совпадают.')
        return password2

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and phone.isdigit() and len(phone) == 12 and phone.startswith('996'):
            return phone
        raise forms.ValidationError('Формат номера телефона неверный.')

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if only_roman_chars(first_name):
            return first_name
        raise forms.ValidationError('Имя должно быть написано на латинице, как в загранпаспорте.')

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if only_roman_chars(last_name):
            return last_name
        raise forms.ValidationError('Фамилия должна быть написана на латинице, как в загранпаспорте.')

    def clean_university(self):
        university_id = self.cleaned_data.get('university')
        university = University.objects.filter(pk=university_id).first()
        if not university:
            raise forms.ValidationError('Университет не найден.')
        return university

    def clean_faculty(self):
        faculty_id = self.cleaned_data.get('faculty')
        faculty = Faculty.objects.filter(pk=faculty_id).first()
        if not faculty:
            raise forms.ValidationError('Университет не найден.')
        return faculty

    def save(self):
        user = User.objects.create_user(
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password'),
            phone=self.cleaned_data.get('phone'),
        )
        profile = Profile.objects.create(
            user=user,
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            bday=self.cleaned_data.get('birthday'),
            university=self.cleaned_data.get('university'),
            faculty=self.cleaned_data.get('faculty'),
        )
        return user, profile


class DocumentTypesForm(forms.Form):
    document_type = forms.CharField(
        widget=forms.Select(
            attrs={'class':  'form-control'},
            choices=DOCUMENT_TYPE_CHOICES),
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('document_type') not in ['training_agreement', 'employment_agreement', 
                                                     'training_stable', 'acts', 'closures', ]:
            self.add_error('document_type', 'Выберите правильный тип документа')
        return cleaned_data


class TrainingAgreementForm(forms.Form):

    admin = forms.IntegerField(
        widget=forms.Select(
            attrs={'class': 'form-control'},
        )
    )
    agreement_cost = forms.ModelChoiceField(queryset=Tariff.objects.all(),
                                            widget=forms.Select(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('admin') not in ContractAdmin.objects.values_list('id', flat=True):
            self.add_error('admin', 'Выберите администратора из списка.')

        return cleaned_data


class TrainingAgreementUnchangeForm(forms.Form):
    admin = forms.IntegerField(
        widget=forms.Select(
            attrs={'class': 'form-control'},
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('admin') not in ContractAdmin.objects.values_list('id', flat=True):
            self.add_error('admin', 'Выберите администратора из списка.')
        return cleaned_data


class AgreementActForm(forms.Form):
    admin = forms.IntegerField(
        widget=forms.Select(
            attrs={'class': 'form-control'},
        )
    )
    agreement_type = forms.CharField(
        widget=forms.Select(
            attrs={'class': 'form-control'},
            choices=AGREEMENT_ACT_TYPE_CHOICES
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('admin') not in ContractAdmin.objects.values_list('id', flat=True):
            self.add_error('admin', 'Выберите администратора из списка.')
        if cleaned_data.get('agreement_type') not in ['training_agreement_act',
                                                      'employment_agreement_act',
                                                      'training_stable_act']:
            self.add_error('agreement_type', 'Выберите правильный тип документа')
        return cleaned_data


class ClosureForm(forms.Form):
    admin = forms.IntegerField(
            widget=forms.Select(
                attrs={'class': 'form-control'},
            )
    )
    agreement_type = forms.CharField(
        widget=forms.Select(
            attrs={'class': 'form-control'},
            choices=CLOSURE_DOC_TYPE_CHOICES
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('admin') not in ContractAdmin.objects.values_list('id', flat=True):
            self.add_error('admin', 'Выберите администратора из списка.')
        if cleaned_data.get('agreement_type') not in ['training_closure',
                                                      'employment_closure',
                                                      'training_stable_closure', ]:
            self.add_error('agreement_type', 'Выберите правильный тип документа')
        return cleaned_data


class CheckboxSelectAdmin(ChoiceWidget):
    allow_multiple_selected = True
    input_type = 'checkbox'
    checked_attribute = {'checked': True}
    template_name = 'admin/groups/multiple_admin_select.html'

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        new_optgroups = {}
        optgroupd_list = []
        for option in context['widget']['optgroups']:
            option[1][0]['verbose_name'] = option[1][0]['label'].split('|')[1]
            option[1][0]['label'] = option[1][0]['label'].split('|')[2]
            if option[1][0]['verbose_name'] not in new_optgroups.keys():
                new_optgroups[option[1][0]['verbose_name']] = [option]
            else:
                new_optgroups[option[1][0]['verbose_name']].append(option)

        optgroupd_list.append({k: v for k, v in new_optgroups.items()})
        context['widget']['optgroups'] = optgroupd_list
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class ManagersListForm(forms.Form):
    manager = forms.ModelChoiceField(queryset=Staff.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
