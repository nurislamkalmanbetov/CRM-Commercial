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
                                          ProfileNotConfirmed, Staff)
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import ManyToManyField
from django.utils.safestring import mark_safe

# from applications.accounts.admin_utils.archive_admin import ProfileInArchiveAdmin
# from applications.accounts.admin_utils.termin_admin import ProfileInTerminAdmin
# from applications.accounts.admin_utils.contact_admin import ProfileInContactDetailsAdmin
# from applications.accounts.admin_utils.embassy_admin import ProfileInEmbassyAdmin
# from applications.accounts.admin_utils.interview_admin import ProfileInterviewAdmin
# from applications.accounts.admin_utils.not_confirmed_admin import ProfileNotConfirmedAdmin
# from applications.accounts.admin_utils.payment_admin import ProfileInPaymentAdmin
# from applications.accounts.admin_utils.profile_admin import ProfileAdmin
# from applications.accounts.admin_utils.registration_admin import ProfileRegistrationAdmin
# from applications.accounts.admin_utils.sending_admin import ProfileInSendingAdmin
# from applications.accounts.admin_utils.vacancy_admin import ProfileInVacancyAdmin
# from applications.accounts.admin_utils.essential_info_admin import ProfileInEssentialInfoAdmin
# from applications.accounts.admin_utils.refused_admin import ProfileInRefusedAdmin





User = get_user_model()



class UserAdmin(admin.ModelAdmin):
    # fields = ['email', 'phone', 'whatsapp_phone', 'password','is_staff','is_employer', 'is_student', 'is_delete', 'is_active', 'is_superuser', ]
    fieldsets = (
        (None, {'fields': ('email', 'avatar','phone', 'whatsapp_phone', 'password','is_staff','is_employer', 'is_student', 'is_delete', 'is_active', 'is_superuser',)}),
            )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone','avatar', 'whatsapp_phone', 'password1','password2','is_staff','is_employer', 'is_student', 'is_delete', 'is_active', 'is_superuser', ),
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


#@admin.register(ProfileHistory)
#class ProfileHistoryAdmin(admin.ModelAdmin):

#    list_display = ['username', 'date', 'changes']
#
#    search_fields = ['username']


#admin.site.register(Staff)

# admin.site.register(ProfileInEssentialInfo, ProfileInEssentialInfoAdmin)

# admin.site.register(ProfileInArchive, ProfileInArchiveAdmin)

# admin.site.register(ProfileInContactDetails, ProfileInContactDetailsAdmin)

# admin.site.register(ProfileInEmbassy, ProfileInEmbassyAdmin)

# admin.site.register(ProfileInInterview, ProfileInterviewAdmin)

# admin.site.register(ProfileNotConfirmed, ProfileNotConfirmedAdmin)

# admin.site.register(ProfileInPayment, ProfileInPaymentAdmin)

# admin.site.register(Profile, ProfileAdmin)

# admin.site.register(ProfileInRegistration, ProfileRegistrationAdmin)

# admin.site.register(ProfileInSending, ProfileInSendingAdmin)

# admin.site.register(ProfileInVacancy, ProfileInVacancyAdmin)

# admin.site.register(ProfileInTermin, ProfileInTerminAdmin)

# admin.site.register(ProfileInRefused, ProfileInRefusedAdmin)

# class ProfileInVacancyAdmin(admin.ModelAdmin):
#     list_display = [
#         'employer',
#     ]
#     autocomplete_fields = ['employer',]

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


admin.site.register(ProfileInArchive)
admin.site.register(ProfileInContactDetails)
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
