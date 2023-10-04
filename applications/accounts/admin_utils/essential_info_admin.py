from django.contrib import admin


class ProfileInEssentialInfoAdmin(admin.ModelAdmin):

    fields = ['first_name', 'last_name', 'level', 'courses_info',  'loan',
              'in_interview_review', 'employer_confirm_date', 'zav_send_date',
              'termin', 'has_termin', 'start_vise_date', 'end_vise_date',
              'in_review', 'visa_reject', 'nvks', ]

    list_display = [
        'first_name',
        'last_name',
    ]

    search_fields = [
        'first_name',
        'last_name',
    ]

    readonly_fields = ('first_name', 'last_name', 'level', 'courses_info',  'loan',
                       'in_interview_review', 'employer_confirm_date', 'zav_send_date',
                       'termin', 'has_termin', 'start_vise_date', 'end_vise_date',
                       'in_review', 'visa_reject', 'nvks', )
