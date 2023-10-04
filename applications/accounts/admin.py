from typing import Any
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from applications.accounts.forms import CheckboxSelectAdmin
from applications.accounts.models import (
    Bill, Interview,
    Payment, Profile, 
    ProfileHistory,
    ProfileInContactDetails,
    ProfileInEmbassy,
    ProfileInEssentialInfo,
    ProfileInInterview, 
    ProfileInVacancy,
    ProfileNotConfirmed, Staff,
    SupportRequest, SupportResponse,
    StudentDocumentsProfileProxy,
    )
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import ManyToManyField
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q


User = get_user_model()


class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    # fields = ['email', 'phone', 'whatsapp_phone', 'password','is_staff','is_employer', 'is_student', 'is_delete', 'is_active', 'is_superuser', ]
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'whatsapp_phone', 'password','is_staff','is_employer', 'is_student', 'is_delete', 'is_active', 'is_superuser',)}),
            )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'whatsapp_phone', 'password1','password2','is_staff','is_employer', 'is_student', 'is_delete', 'is_active', 'is_superuser', ),
        }),
    )
    list_display = ['id','email', 'phone', 'whatsapp_phone', 'is_staff', 'is_delete', 'is_active','is_employer', 'is_student', 'is_superuser', ]
    search_fields = ['email', 'phone', 'whatsapp_phone', ]
    list_editable = ['is_staff', 'is_delete', 'is_active','is_employer', 'is_student', 'is_superuser',]

    class Meta:
        model = User


class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'user',
        'content_type',
        'action_flag',
        'object_repr',
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'object_repr',
        'change_message',
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
        'change_message',
    ]


class ProfileHistoryAdmin(admin.ModelAdmin):

    list_display = ['username', 'date', 'changes']

    search_fields = ['username']


class ProfileInVacancyAdmin(admin.ModelAdmin):
    list_display = [
        'employer',
    ]
    autocomplete_fields = ['employer',]


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'photo', 'first_name', 'last_name', 'telephone',
        'bday', 'gender','been_to_germany', 'nationality', 'birth_country','reg_apartment',

        )
    fieldsets = (
        (None, {'fields': ('user', 'photo', 'first_name', 'last_name', 'telephone',
        'bday', 'gender','been_to_germany', 'nationality', 'birth_country','reg_apartment',
        'university','faculty','study_start','study_end','direction',
        'german', 'english', 'turkish', 'russian', 'chinese', 
        'driver_license', 'driving_experience', 'cat_a', 'cat_b', 'cat_c', 'cat_d', 'cat_e', 'tractor', 'transmission', 
        'reading', 'singing', 'travelling', 'yoga', 'dancing', 'sport', 'drawing', 'computer_games', 'guitar', 'films', 'music', 'knitting', 'cooking', 'fishing', 'photographing', 
        )}),
            )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'photo', 'first_name', 'last_name', 'telephone',
        'bday', 'gender','been_to_germany', 'nationality', 'birth_country','reg_apartment',
        'university','faculty','study_start','study_end','direction',
        'german', 'english', 'turkish', 'russian', 'chinese', 
        'driver_license', 'driving_experience', 'cat_a', 'cat_b', 'cat_c', 'cat_d', 'cat_e', 'tractor', 'transmission', 
        'reading', 'singing', 'travelling', 'yoga', 'dancing', 'sport', 'drawing', 'computer_games', 'guitar', 'films', 'music', 'knitting', 'cooking', 'fishing', 'photographing', 
        ),
        }),
    )


    class Meta:
        model = Profile


class SupportResponseInline(admin.StackedInline): 
    model = SupportResponse
    extra = 1


class SupportRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('message',)  

    fieldsets = (
        (None, {'fields': ('user', 'message', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user',),
        }),
    )
    def response_sent(self, obj):
    
        response = obj.response.first()
        if response and response.sent:
            return format_html('<span style="color: green;">&#10004;</span>')  # Зеленая галочка
        return format_html('<span style="color: red;">&#10008;</span>')  # Красный крестик
    response_sent.short_description = 'Отправлено'
    list_display = ('id','user', 'message', 'created_at', 'response_sent')
    inlines = [SupportResponseInline]


class PaymentAdminForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ограничьте выбор "Оплату принял" только сотрудниками и суперпользователем
        self.fields['who_created'].queryset = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))


class PaymentAdmin(admin.ModelAdmin):
    form = PaymentAdminForm
    list_display = ['id', 'user', 'who_created', 'amount_paid', 'remaining_amount', 'is_fully_paid', 'payment_date', 'due_date']


class StudentDocumentsAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'user_email', 'count_uploaded_documents', 'count_remaining_documents']
    search_fields = ['user__email']

    fieldsets = (
        (None, {
            'fields': (
                'user',
                'photo', 'study_certificate', 'study_certificate_embassy', 'study_certificate_translate_embassy',
                'photo_for_schengen', 'zagranpassport_copy', 'passport_copy', 'fluorography_express',
                'fluorography', 'immatrikulation', 'transcript', 'transcript_translate', 'bank_statement',
                'conduct_certificate', 'mentaldispanser_certificate', 'drugdispanser_certificate', 'parental_permission',
                'bank_details', 'agreement1', 'agreement2', 'agreement3', 'act1', 'act2', 'act3', 
                'closure1', 'closure2', 'closure3', 'consult_list', 'invitation', 'labor_agreement', 
                'liveplace_approve', 'insurance', 'visa_file'
            )
        }),
    )

    def user_id(self, obj):
        return obj.user.id

    user_id.short_description = 'ID пользователя'

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email пользователя'

    def count_documents(self, obj):
        fields = [
            obj.photo, obj.study_certificate, obj.study_certificate_embassy, 
            # ... и так далее для всех других полей ...
            obj.visa_file
        ]
        return sum(1 for field in fields if field)

    def count_uploaded_documents(self, obj):
        return self.count_documents(obj)

    count_uploaded_documents.short_description = 'Загруженные документы'

    def count_remaining_documents(self, obj):
        total_documents = 29  # общее количество полей документов
        uploaded = self.count_uploaded_documents(obj)
        return total_documents - uploaded

    count_remaining_documents.short_description = 'Оставшиеся документы'




class ProfileInContactDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_user_email', 'get_user_phone', 'get_user_whatsapp_phone', 'get_father_phone', 'get_mother_phone']

    def get_user_email(self, obj):
        return obj.user.email
    
    get_user_email.short_description = "User Email"

    def get_user_phone(self, obj):
        return obj.user.phone 
    
    get_user_phone.short_description = "User Phone"
    
    def get_user_whatsapp_phone(self, obj):
        whatsapp_phone = obj.user.whatsapp_phone
        if whatsapp_phone:
            return format_html('<a href="https://{}" target="_blank">{}</a>'.format("wa.me/+" + whatsapp_phone, whatsapp_phone))
        return None

    get_user_whatsapp_phone.short_description = 'User WhatsApp Phone'

    def get_father_phone(self, obj):
        return obj.father_phone

    get_father_phone.short_description = 'Father Phone'

    def get_mother_phone(self, obj):
        return obj.mother_phone

    get_mother_phone.short_description = 'Mother Phone'
    

admin.site.register(ProfileInContactDetails, ProfileInContactDetailsAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Staff)
admin.site.register(StudentDocumentsProfileProxy, StudentDocumentsAdmin)
admin.site.register(SupportRequest, SupportRequestAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(ProfileHistory,ProfileHistoryAdmin)
admin.site.register(LogEntry,LogEntryAdmin)
admin.site.register(ProfileInEmbassy)
admin.site.register(ProfileInInterview)
admin.site.register(ProfileNotConfirmed)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(ProfileInVacancy, ProfileInVacancyAdmin)