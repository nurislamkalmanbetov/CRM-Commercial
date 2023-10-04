from django.contrib import admin

from .models import *
from applications.accounts.admin_utils.inlines import VacancyInline


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ru', 'name_de', 'address', 'phone', 'site', )


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    pass


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass


@admin.register(ContractAdmin)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'gender', 'patent_id', 'patent_date', 'given_by', ]

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'ФИО'


@admin.register(EmployerCompany)
class EmployerCompanyAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'country']

    list_display = ['id', 'name', 'user', 'country', ]

    search_fields = ['name']

    inlines = [VacancyInline]


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display =  [
        'id', 'name', 'language', 'user', 'employer_company', 'required_positions', 'salary', 'city', 'destination_point'
    ]



@admin.register(ProfileCounter)
class ProfileCounterAdmin(admin.ModelAdmin):
    list_display = ['creation_date', 'amount_of_profiles', ]


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    fields = (('amount_in_digits', 'amount_in_text'), )

    list_display = ['amount_in_digits', ]


@admin.register(ReviewVacancy)
class ReviewVacancyAdmin(admin.ModelAdmin):
    list_display = ['status','applicant_profile','employer','vacancy','employer_comment']

    search_fields = ['status']


@admin.register(CompanyReview)
class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = ('company', 'user', 'rating', 'is_review_confirmed', 'created_date')
    list_filter = ('rating', 'is_review_confirmed', 'created_date')
    search_fields = ('company__name', 'user__email', 'comment')  # предполагается, что у EmployerCompany есть поле name и у User есть поле email
    list_editable = ('is_review_confirmed',)
    readonly_fields = ('created_date', 'user', 'company', 'rating', 'comment') # чтобы некоторые поля были только для чтения
    date_hierarchy = 'created_date'
    ordering = ('-created_date', 'company')


