from django.contrib import admin
from django.utils.timezone import localtime
from django import forms

from applications.accounts.models import Bill, Interview
from applications.core.models import Notification, Vacancy, EmployerCompany


class InterviewForm(forms.ModelForm):

    model = Interview
    fields = ['company', 'vacancy', 'city', 'invited_status', 'invite_date', 'student_confirm' 
              'vacancy_confirm', 'appointment_date', 'work_from', 'work_to',
              ]

    widgets = {
        'company': forms.Select(attrs={'class': 'company_input', }),
        'vacancy': forms.Select(attrs={'class': 'vacancy_input', }),

    }


class AbstractInterviewInline(admin.StackedInline):
    form = InterviewForm


class NotificationsInline(admin.StackedInline):
    model = Notification
    extra = 1


class VacancyInline(admin.StackedInline):
    model = Vacancy
    extra = 1
    field = ['picture', 'name', 'salary', 'city', 'accomodation_type']

    


class InterviewInline(AbstractInterviewInline):
    extra = 1
    model = Interview
    # fields = ['company', 'vacancy', ]


class BillInline(admin.StackedInline):
    model = Bill
    extra = 1
    fields = ['pay_sum', 'pay_date', 'who_created']
    readonly_fields = ['pay_date', 'who_created']

    def pay_date(self, obj):
        return localtime(obj.created_at).strftime("%d.%m.%Y, %H:%M")

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('accounts.delete_bill')

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('accounts.change_bill')

    def save_model(self, request, obj, form, change):
        obj.who_created = request.user
        obj.save()

    pay_date.short_description = 'Время оплаты'





