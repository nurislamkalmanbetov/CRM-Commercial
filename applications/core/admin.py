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

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display =  [
        'id', 'name', 'language', 'user', 'employer_company', 'required_positions', 'salary', 'city', 'destination_point','is_vacancy_confirmed','created_date',
    ]
    list_editable =('is_vacancy_confirmed',)
    date_hierarchy = 'created_date'


@admin.register(EmployerCompany)
class EmployerCompanyAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'country', 'description',]

    list_display = ['id', 'name', 'user', 'country', 'description',]

    search_fields = ['name', ]

@admin.register(CompanyReview)
class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = ('company', 'user', 'rating', 'is_review_confirmed', 'created_date')
    list_filter = ('rating', 'is_review_confirmed', 'created_date')
    search_fields = ('company__name', 'user__email', 'comment')  # предполагается, что у `EmployerCompany` есть поле `name` и у `User` есть поле `email`
    list_editable = ('is_review_confirmed',)
    readonly_fields = ('created_date', 'user', 'company', 'rating', 'comment') # чтобы некоторые поля были только для чтения
    date_hierarchy = 'created_date'
    ordering = ('-created_date', 'company')

@admin.register(ProfileCounter)
class ProfileCounterAdmin(admin.ModelAdmin):
    list_display = ['creation_date', 'amount_of_profiles', ]


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    fields = (('amount_in_digits', 'amount_in_text'), )

    list_display = ['amount_in_digits', ]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'created_at', 'status')
    list_filter = ('status',)
    search_fields = ('text', )
    list_editable = ('status',)
    actions = ['mark_as_DECLINED', 'mark_as_modereted']

    def mark_as_DECLINED(self, request, queryset):
        queryset.update(status='DECLINED')
    mark_as_DECLINED.short_description = 'Пометить как в Отклонен'
    def mark_as_modereted(self, request, queryset):
        queryset.update(status='MODERETED')
    mark_as_modereted.short_description = 'Пометить как в прошли модерацию'

@admin.register(ImprovementIdea)
class ImprovementIdeaAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'created_at', 'status')
    list_filter = ('status',)
    search_fields = ('text',)