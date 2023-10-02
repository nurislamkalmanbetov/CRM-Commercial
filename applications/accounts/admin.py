from applications.accounts.forms import CheckboxSelectAdmin
from applications.accounts.models import (Bill, Interview, Profile,
                                          ProfileHistory, ProfileInArchive,
                                          ProfileInContactDetails,
                                          ProfileInEmbassy,
                                          ProfileInEssentialInfo,
                                          ProfileInInterview, ProfileInPayment,
                                          ProfileInRefused,
                                          ProfileInRegistration,
                                          ProfileInSending, ProfileInTermin,
                                          ProfileInVacancy,
                                          ProfileNotConfirmed, Staff, Payment, StudentDocumentsProfileProxy)
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import ManyToManyField
from django.utils.safestring import mark_safe
from .forms import PaymentAdminForm




User = get_user_model()



class UserAdmin(admin.ModelAdmin):
    # fields = ['email', 'phone', 'whatsapp_phone', 'password','is_staff','is_employer', 'is_student', 'is_delete', 'is_active', 'is_superuser', ]
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'whatsapp_phone', 'password','is_staff','is_employer', 'is_student', 'is_delete', 'is_active', 'is_superuser',)}),
            )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone','whatsapp_phone', 'password1','password2','is_staff','is_employer', 'is_student', 'is_delete', 'is_active', 'is_superuser', ),
        }),
    )
    list_display = ['id','email', 'phone', 'whatsapp_phone', 'is_staff', 'is_delete', 'is_active','is_employer', 'is_student', 'is_superuser', ]
    search_fields = ['email', 'phone', 'whatsapp_phone', ]
    list_editable = ['is_staff', 'is_delete', 'is_active','is_employer', 'is_student', 'is_superuser',]

    def icon(self, obj):
        if obj.avatar:
            return mark_safe(f'<a href="{obj.avatar.url}" target="_blank"><img src="{obj.avatar.url}" width="65" height="80"></a>')

    class Meta:
        model = User


admin.site.register(User, UserAdmin)


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    change_list_template = 'admin/change_list.html'
    change_form_template = 'admin/change_form.html'

    list_display = [
        'profile',
        'who_created',
        'pay_sum',
        'created_at',
        'updated_at',
    ]

    fields = [
        'profile',
        'who_created',
        'pay_sum',
        'created_at',
        'updated_at',
    ]

    readonly_fields = ["who_created", "created_at", "updated_at"]

    search_fields = [
        'who_created__email',
        'profile__user__email',
    ]

    list_filter = [
        'created_at',
        'updated_at',
    ]

    def save_model(self, request, obj, form, change):
        obj.who_created = request.user
        obj.save()

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions

from django.contrib.admin.models import LogEntry


@admin.register(LogEntry)
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



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'photo', 'first_name', 'last_name', 'telephone',
        'bday', 'gender','been_to_germany', 'nationality', 'birth_country','reg_apartment',
        'university','faculty','study_start','study_end','direction',
        'german', 'english', 'turkish', 'russian', 'chinese', 
        'driver_license', 'driving_experience', 'cat_a', 'cat_b', 'cat_c', 'cat_d', 'cat_e', 'tractor', 'transmission', 
        'reading', 'singing', 'travelling', 'yoga', 'dancing', 'sport', 'drawing', 'computer_games', 'guitar', 'films', 'music', 'knitting', 'cooking', 'fishing', 'photographing', 
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

class ProfileInContactDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_user_email', 'get_user_phone', 'get_user_whatsapp_phone', 'get_father_phone', 'get_mother_phone']

    def get_user_email(self, obj):
        return obj.user.email
    
    get_user_email.short_description = "User Email"

    def get_user_phone(self, obj):
        return obj.user.phone 
    
    get_user_phone.short_description = "User Phone"
    def get_user_whatsapp_phone(self, obj):
        return obj.user.whatsapp_phone  # Подразумевается, что в модели User есть поле whatsapp_phone

    get_user_whatsapp_phone.short_description = 'User WhatsApp Phone'

    def get_father_phone(self, obj):
        return obj.father_phone  # Подразумевается, что в модели Profile есть поле father_phone

    get_father_phone.short_description = 'Father Phone'

    def get_mother_phone(self, obj):
        return obj.mother_phone  # Подразумевается, что в модели Profile есть поле mother_phone

    get_mother_phone.short_description = 'Mother Phone'



class PaymentAdmin(admin.ModelAdmin):
    form = PaymentAdminForm
    list_display = ['id', 'user', 'who_created', 'amount_paid', 'remaining_amount', 'is_fully_paid', 'payment_date', 'due_date']

class StudentDocumentsAdmin(admin.ModelAdmin):
    list_display = [ 'user',
        'photo', 'study_certificate_embassy_short', 'study_certificate_embassy', 'study_certificate_translate_embassy',
        'photo_for_schengen', 'zagranpassport_copy', 'passport_copy', 'fluorography_express',
        'fluorography', 'immatrikulation', 'transcript', 'transcript_translate', 'bank_statement',
        'conduct_certificate', 'mentaldispanser_certificate', 'drugdispanser_certificate', 'parental_permission',
        'bank_details', 'agreement1', 'agreement2', 'agreement3', 'act1', 'act2', 'act3', 
        'closure1', 'closure2', 'closure3', 'consult_list', 'invitation', 'labor_agreement', 
        'liveplace_approve', 'insurance', 'visa_file'
    ]
    search_fields = ['user__email'] 

    def study_certificate_embassy_short(self, obj):
        if obj.study_certificate_embassy:
            return str(obj.study_certificate_embassy)[:10] + "..."
        return ""
    study_certificate_embassy_short.short_description = 'Справка'

admin.site.register(StudentDocumentsProfileProxy, StudentDocumentsAdmin)

admin.site.register(Payment,PaymentAdmin)

admin.site.register(ProfileInContactDetails,ProfileInContactDetailsAdmin)

admin.site.register(ProfileInArchive)
# admin.site.register(ProfileInContactDetails)
admin.site.register(ProfileInEmbassy)
admin.site.register(ProfileInInterview)
admin.site.register(ProfileNotConfirmed)
admin.site.register(ProfileInPayment)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileInRegistration)
admin.site.register(ProfileInSending)
# admin.site.register(ProfileInVacancy, ProfileInVacancyAdmin)
admin.site.register(ProfileInTermin)
admin.site.register(ProfileInRefused)
