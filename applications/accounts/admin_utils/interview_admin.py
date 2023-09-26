import re

from django.contrib import admin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from .inlines import NotificationsInline, InterviewInline
from applications.accounts.models import Profile
from applications.accounts import filters
from applications.accounts.filters import CustomDateFilter
from applications.accounts.utils import get_mark_safe


class ProfileInterviewAdmin(admin.ModelAdmin):
    inlines = [
        NotificationsInline,
        InterviewInline,
    ]

    readonly_fields = ['payment']
    fields = [
        'first_name', 'last_name', 'bday', 'in_interview_review', 'passport_number', 'zagranpassport_number', 'zagranpassport_end_time',
        'embassy_visametric', 'termin', 'university', 'faculty', 'year', 'summer_holidays_end', 'zagranpassport_copy',
        'immatrikulation', 'payment', 'accomodation_type', 'employer_confirm_date', 'zav_send_date',
    ]

    list_display = [
        'whatsapp_link',
        'nvks_custom',
        'full_name_reverse',
        'note_form',
        'comment_form',
        'bday',
        'zagranpassport_number_id',
        'zagranpassport_end_time_admin',
        'termin_date',
        'termin_time',
        'passport_number_id',
        'gender',
        'summer_holidays_start',
        'summer_holidays_end',
        'university',
        'faculty',
        'year',
        'phone',
        'level',
        'courses_info',

        'sob1_company_name',
        'sob1_position',
        'sob1_invited_status',
        'sob1_appointment_date',
        'sob1_vacancy_confirm',
        'sob1_student_confirm',
        'sob1_holidays_period',

        'sob2_company_name',
        'sob2_position',
        'sob2_invited_status',
        'sob2_appointment_date',
        'sob2_vacancy_confirm',
        'sob2_student_confirm',
        'sob2_holidays_period',

        'sob3_company_name',
        'sob3_position',
        'sob3_invited_status',
        'sob3_appointment_date',
        'sob3_vacancy_confirm',
        'sob3_student_confirm',
        'sob3_holidays_period',

        'sob4_company_name',
        'sob4_position',
        'sob4_invited_status',
        'sob4_appointment_date',
        'sob4_vacancy_confirm',
        'sob4_student_confirm',
        'sob4_holidays_period',

        'sob5_company_name',
        'sob5_position',
        'sob5_invited_status',
        'sob5_appointment_date',
        'sob5_vacancy_confirm',
        'sob5_student_confirm',
        'sob5_holidays_period',

        'sob6_company_name',
        'sob6_position',
        'sob6_invited_status',
        'sob6_appointment_date',
        'sob6_vacancy_confirm',
        'sob6_student_confirm',
        'sob6_holidays_period',

        'sob7_company_name',
        'sob7_position',
        'sob7_invited_status',
        'sob7_appointment_date',
        'sob7_vacancy_confirm',
        'sob7_student_confirm',
        'sob7_holidays_period',

        'sob8_company_name',
        'sob8_position',
        'sob8_invited_status',
        'sob8_appointment_date',
        'sob8_vacancy_confirm',
        'sob8_student_confirm',
        'sob8_holidays_period',
    ]

    search_fields = [
        'first_name',
        'last_name',
        'user__phone',
        'passport_number',
        'zagranpassport_number',
    ]

    list_filter = [
        'gender',
        'university',
        'faculty',
        'year',
        filters.DirectionFilter,
        ('summer_holidays_start', CustomDateFilter),
        ('summer_holidays_end', CustomDateFilter),
        ('study_start', CustomDateFilter),
        ('study_end', CustomDateFilter)
    ]

    change_list_template = 'admin/accounts/change_list.html'

    class Media:
        css = {
            'all': ('admin/css/changelists_custom.css',)
        }

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _interview_count=Count("interviews", distinct=True),
        )
        return queryset

    def changelist_view(self, request, extra_context=None):

        if request.GET.get('get_xls', None):
            return self.export_xls(request)

        extra_context = extra_context or {}
        extra_context['table_classname'] = 'interview'
        return super(ProfileInterviewAdmin, self).changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        profile = get_object_or_404(Profile, pk=object_id)
        if profile and profile.photo:
            extra_context['photo_url'] = profile.photo.url
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def passport_number_id(self, obj,  xls=False):
        return obj.passport_number

    def zagranpassport_number_id(self, obj, xls=False):
        return obj.zagranpassport_number

    def zagranpassport_end_time_admin(self, obj, xls=False):
        return obj.zagranpassport_end_time

    def whatsapp_link(self, obj):
        return mark_safe(
            f'<a href="https://api.whatsapp.com/send?phone={obj.user.whatsapp_phone}" target="_blank" title="Написать на {obj.user.whatsapp_phone}"><img src="/static/images/icons/whatsapp.svg" width="18" height="18" /></a>')

    def full_name_reverse(self, obj):
        return mark_safe(
            f'<a href="/admin/accounts/profileininterview/{obj.id}/change?next=/admin/accounts/profileininterview/" title="{obj.full_name_reverse}">{obj.full_name_reverse}</a>')

    def note_form(self, obj):
        action = '/api/v1/update_note/'
        return mark_safe(f'''<div class="note_form" data-action="{action}" data-user-id="{obj.id}">
                                    <span class="note_form_text">{obj.note}</span>
                                    <input class="note_form__input" type="text" value="{obj.note}" name="note" />
                                    <button class="note_form__button"><img src="/static/images/icons/save.svg" width="18" height="18" /></button>
                                </div>''')
    
    def comment_form(self, obj):
        action = '/api/v1/update_comment/'
        return mark_safe(f'''<div class="comment_form" data-action="{action}" data-user-id="{obj.id}">
                                    <span class="note_form_text">{obj.comment}</span>
                                    <input class="comment_form__input" type="text" value="{obj.comment}" name="comment" />
                                    <button class="comment_form__button"><img src="/static/images/icons/save.svg" width="18" height="18" /></button>
                                </div>''')

    def phone(self, obj, xls=False):
        return obj.user.phone

    def termin_date(self, obj, xls=False):
        return obj.termin.strftime('%d.%m.%y') if obj.termin else '-'

    def termin_time(self, obj, xls=False):
        return obj.termin.strftime('%H:%M') if obj.termin else '-'

    def sob1_company_name(self, obj, xls=False):
        interview = None
        if obj._interview_count > 0:
            interview = obj.interviews.all().order_by('id').first()
        return interview.company.name if interview else '-'

    def sob1_position(self, obj, xls=False):
        interview = None
        if obj._interview_count > 0:
            interview = obj.interviews.all().order_by('id').first()
        return interview.vacancy.name if interview else '-'

    def sob1_invited_status(self, obj, xls=False):
        interview = None
        if obj._interview_count > 0:
            interview = obj.interviews.all().order_by('id').first()

        if interview and interview.invited_status == 'not_invited':
            return get_mark_safe(0)
        elif interview and interview.invited_status == 'doubtful':
            return get_mark_safe(3)
        elif interview and interview.invited_status == 'invited':
            return get_mark_safe(1)
        elif interview and interview.invited_status == 'invited_twice':
            return get_mark_safe(2)
        return get_mark_safe(0)

    def sob1_appointment_date(self, obj, xls=False):
        interview = None
        if obj._interview_count > 0:
            qs = obj.interviews.all().order_by('id')
            interview = qs.first() if qs.count() > 0 else None
        return interview.appointment_date.strftime('%d.%m.%y %H:%M') if interview and interview.appointment_date else '-'

    def sob1_vacancy_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 0:
            qs = obj.interviews.all().order_by('id')
            interview = qs.first() if qs.count() > 0 else None
        return get_mark_safe(1) if interview and interview.vacancy_confirm else get_mark_safe(0)

    def sob1_student_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 0:
            qs = obj.interviews.all().order_by('id')
            interview = qs.first() if qs.count() > 0 else None
        return get_mark_safe(1) if interview and interview.student_confirm else get_mark_safe(0)

    def sob1_holidays_period(self, obj, xls=False):
        return f'{obj.summer_holidays_start.strftime("%d.%m.%y")}-{obj.summer_holidays_end.strftime("%d.%m.%y")}' \
            if obj.summer_holidays_start and obj.summer_holidays_end else '-'

    def sob2_company_name(self, obj, xls=False):
        interview = None
        if obj._interview_count > 1:
            qs = obj.interviews.all().order_by('id')
            interview = qs[1] if qs.count() > 1 else None
        return interview.company.name if interview else '-'

    def sob2_position(self, obj, xls=False):
        interview = None
        if obj._interview_count > 1:
            qs = obj.interviews.all().order_by('id')
            interview = qs[1] if qs.count() > 1 else None
        return interview.vacancy.name if interview else '-'

    def sob2_invited_status(self, obj, xls=False):
        if obj._interview_count > 1:
            qs = obj.interviews.all().order_by('id')
            interview = qs[1] if qs.count() > 1 else None
            if interview and interview.invited_status == 'not_invited':
                return get_mark_safe(0)
            elif interview and interview.invited_status == 'doubtful':
                return get_mark_safe(3)
            elif interview and interview.invited_status == 'invited':
                return get_mark_safe(1)
            elif interview and interview.invited_status == 'invited_twice':
                return get_mark_safe(2)
        return get_mark_safe(0)

    def sob2_appointment_date(self, obj, xls=False):
        interview = None
        if obj._interview_count > 1:
            qs = obj.interviews.all().order_by('id')
            interview = qs[1] if qs.count() > 1 else None
        return interview.appointment_date.strftime('%d.%m.%y %H:%M') if interview and interview.appointment_date else '-'

    def sob2_vacancy_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 1:
            qs = obj.interviews.all().order_by('id')
            interview = qs[1] if qs.count() > 1 else None
        return get_mark_safe(1) if interview and interview.vacancy_confirm else get_mark_safe(0)

    def sob2_student_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 1:
            qs = obj.interviews.all().order_by('id')
            interview = qs[1] if qs.count() > 1 else None
        return get_mark_safe(1) if interview and interview.student_confirm else get_mark_safe(0)

    def sob2_holidays_period(self, obj, xls=False):
        return f'{obj.summer_holidays_start.strftime("%d.%m.%y")}-{obj.summer_holidays_end.strftime("%d.%m.%y")}' if obj.summer_holidays_start and obj.summer_holidays_end else '-'

    def sob3_company_name(self, obj, xls=False):
        interview = None
        if obj._interview_count > 2:
            qs = obj.interviews.all().order_by('id')
            interview = qs[2] if qs.count() > 2 else None
        return interview.company.name if interview else '-'

    def sob3_position(self, obj, xls=False):
        interview = None
        if obj._interview_count > 2:
            qs = obj.interviews.all().order_by('id')
            interview = qs[2] if qs.count() > 2 else None
        return interview.vacancy.name if interview else '-'

    def sob3_invited_status(self, obj, xls=False):
        if obj._interview_count > 2:
            qs = obj.interviews.all().order_by('id')
            interview = qs[2] if qs.count() > 2 else None
            if interview and interview.invited_status == 'not_invited':
                return get_mark_safe(0)
            elif interview and interview.invited_status == 'doubtful':
                return get_mark_safe(3)
            elif interview and interview.invited_status == 'invited':
                return get_mark_safe(1)
            elif interview and interview.invited_status == 'invited_twice':
                return get_mark_safe(2)
        return get_mark_safe(0)

    def sob3_appointment_date(self, obj, xls=False):
        interview = None
        if obj._interview_count > 2:
            qs = obj.interviews.all().order_by('id')
            interview = qs[2] if qs.count() > 2 else None
        return interview.appointment_date.strftime('%d.%m.%y %H:%M') if interview and interview.appointment_date else '-'

    def sob3_vacancy_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 2:
            qs = obj.interviews.all().order_by('id')
            interview = qs[2] if qs.count() > 2 else None
        return get_mark_safe(1) if interview and interview.vacancy_confirm else get_mark_safe(0)

    def sob3_student_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 2:
            qs = obj.interviews.all().order_by('id')
            interview = qs[2] if qs.count() > 2 else None
        return get_mark_safe(1) if interview and interview.student_confirm else get_mark_safe(0)

    def sob3_holidays_period(self, obj, xls=False):
        return f'{obj.summer_holidays_start.strftime("%d.%m.%y")}-{obj.summer_holidays_end.strftime("%d.%m.%y")}' if obj.summer_holidays_start and obj.summer_holidays_end else '-'

    def sob4_company_name(self, obj, xls=False):
        interview = None
        if obj._interview_count > 3:
            qs = obj.interviews.all().order_by('id')
            interview = qs[3] if qs.count() > 3 else None
        return interview.company.name if interview else '-'

    def sob4_position(self, obj, xls=False):
        interview = None
        if obj._interview_count > 3:
            qs = obj.interviews.all().order_by('id')
            interview = qs[3] if qs.count() > 3 else None
        return interview.vacancy.name if interview else '-'

    def sob4_invited_status(self, obj, xls=False):
        if obj._interview_count > 3:
            qs = obj.interviews.all().order_by('id')
            interview = qs[3] if qs.count() > 3 else None
            if interview and interview.invited_status == 'not_invited':
                return get_mark_safe(0)
            elif interview and interview.invited_status == 'doubtful':
                return get_mark_safe(3)
            elif interview and interview.invited_status == 'invited':
                return get_mark_safe(1)
            elif interview and interview.invited_status == 'invited_twice':
                return get_mark_safe(2)
        return get_mark_safe(0)

    def sob4_appointment_date(self, obj, xls=False):
        interview = None
        if obj._interview_count > 3:
            qs = obj.interviews.all().order_by('id')
            interview = qs[3] if qs.count() > 3 else None
        return interview.appointment_date.strftime('%d.%m.%y %H:%M') if interview and interview.appointment_date else '-'

    def sob4_vacancy_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 3:
            qs = obj.interviews.all().order_by('id')
            interview = qs[3] if qs.count() > 3 else None
        return get_mark_safe(1) if interview and interview.vacancy_confirm else get_mark_safe(0)

    def sob4_student_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 3:
            qs = obj.interviews.all().order_by('id')
            interview = qs[3] if qs.count() > 3 else None
        return get_mark_safe(1) if interview and interview.student_confirm else get_mark_safe(0)

    def sob4_holidays_period(self, obj, xls=False):
        return f'{obj.summer_holidays_start.strftime("%d.%m.%y")}-{obj.summer_holidays_end.strftime("%d.%m.%y")}' if obj.summer_holidays_start and obj.summer_holidays_end else '-'

    def sob5_company_name(self, obj, xls=False):
        interview = None
        if obj._interview_count > 4:
            qs = obj.interviews.all().order_by('id')
            interview = qs[4] if qs.count() > 4 else None
        return interview.company.name if interview else '-'

    def sob5_position(self, obj, xls=False):
        interview = None
        if obj._interview_count > 4:
            qs = obj.interviews.all().order_by('id')
            interview = qs[4] if qs.count() > 4 else None
        return interview.vacancy.name if interview else '-'

    def sob5_invited_status(self, obj, xls=False):
        if obj._interview_count > 4:
            qs = obj.interviews.all().order_by('id')
            interview = qs[4] if qs.count() > 4 else None
            if interview and interview.invited_status == 'not_invited':
                return get_mark_safe(0)
            elif interview and interview.invited_status == 'doubtful':
                return get_mark_safe(3)
            elif interview and interview.invited_status == 'invited':
                return get_mark_safe(1)
            elif interview and interview.invited_status == 'invited_twice':
                return get_mark_safe(2)
        return get_mark_safe(0)

    def sob5_appointment_date(self, obj, xls=False):
        interview = None
        if obj._interview_count > 4:
            qs = obj.interviews.all().order_by('id')
            interview = qs[4] if qs.count() > 4 else None
        return interview.appointment_date.strftime('%d.%m.%y %H:%M') if interview and interview.appointment_date else '-'

    def sob5_vacancy_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 4:
            qs = obj.interviews.all().order_by('id')
            interview = qs[4] if qs.count() > 4 else None
        return get_mark_safe(1) if interview and interview.vacancy_confirm else get_mark_safe(0)

    def sob5_student_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 4:
            qs = obj.interviews.all().order_by('id')
            interview = qs[4] if qs.count() > 4 else None
        return get_mark_safe(1) if interview and interview.student_confirm else get_mark_safe(0)

    def sob5_holidays_period(self, obj, xls=False):
        return f'{obj.summer_holidays_start.strftime("%d.%m.%y")}-{obj.summer_holidays_end.strftime("%d.%m.%y")}' if obj.summer_holidays_start and obj.summer_holidays_end else '-'

    def sob6_company_name(self, obj, xls=False):
        interview = None
        if obj._interview_count > 5:
            qs = obj.interviews.all().order_by('id')
            interview = qs[5] if qs.count() > 5 else None
        return interview.company.name if interview else '-'

    def sob6_position(self, obj, xls=False):
        interview = None
        if obj._interview_count > 5:
            qs = obj.interviews.all().order_by('id')
            interview = qs[5] if qs.count() > 5 else None
        return interview.vacancy.name if interview else '-'

    def sob6_invited_status(self, obj, xls=False):
        if obj._interview_count > 5:
            qs = obj.interviews.all().order_by('id')
            interview = qs[5] if qs.count() > 5 else None
            if interview and interview.invited_status == 'not_invited':
                return get_mark_safe(0)
            elif interview and interview.invited_status == 'doubtful':
                return get_mark_safe(3)
            elif interview and interview.invited_status == 'invited':
                return get_mark_safe(1)
            elif interview and interview.invited_status == 'invited_twice':
                return get_mark_safe(2)
        return get_mark_safe(0)

    def sob6_appointment_date(self, obj, xls=False):
        interview = None
        if obj._interview_count > 5:
            qs = obj.interviews.all().order_by('id')
            interview = qs[5] if qs.count() > 5 else None
        return interview.appointment_date.strftime('%d.%m.%y %H:%M') if interview and interview.appointment_date else '-'

    def sob6_vacancy_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 5:
            qs = obj.interviews.all().order_by('id')
            interview = qs[5] if qs.count() > 5 else None
        return get_mark_safe(1) if interview and interview.vacancy_confirm else get_mark_safe(0)

    def sob6_student_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 5:
            qs = obj.interviews.all().order_by('id')
            interview = qs[5] if qs.count() > 5 else None
        return get_mark_safe(1) if interview and interview.student_confirm else get_mark_safe(0)

    def sob6_holidays_period(self, obj, xls=False):
        return f'{obj.summer_holidays_start.strftime("%d.%m.%y")}-{obj.summer_holidays_end.strftime("%d.%m.%y")}' if obj.summer_holidays_start and obj.summer_holidays_end else '-'

    def sob7_company_name(self, obj, xls=False):
        interview = None
        if obj._interview_count > 6:
            qs = obj.interviews.all().order_by('id')
            interview = qs[6] if qs.count() > 6 else None
        return interview.company.name if interview else '-'

    def sob7_position(self, obj, xls=False):
        interview = None
        if obj._interview_count > 6:
            qs = obj.interviews.all().order_by('id')
            interview = qs[6] if qs.count() > 6 else None
        return interview.vacancy.name if interview else '-'

    def sob7_invited_status(self, obj, xls=False):
        if obj._interview_count > 6:
            qs = obj.interviews.all().order_by('id')
            interview = qs[6] if qs.count() > 6 else None
            if interview and interview.invited_status == 'not_invited':
                return get_mark_safe(0)
            elif interview and interview.invited_status == 'doubtful':
                return get_mark_safe(3)
            elif interview and interview.invited_status == 'invited':
                return get_mark_safe(1)
            elif interview and interview.invited_status == 'invited_twice':
                return get_mark_safe(2)
        return get_mark_safe(0)

    def sob7_appointment_date(self, obj, xls=False):
        interview = None
        if obj._interview_count > 6:
            qs = obj.interviews.all().order_by('id')
            interview = qs[6] if qs.count() > 6 else None
        return interview.appointment_date.strftime('%d.%m.%y %H:%M') if interview and interview.appointment_date else '-'

    def sob7_vacancy_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 6:
            qs = obj.interviews.all().order_by('id')
            interview = qs[6] if qs.count() > 6 else None
        return get_mark_safe(1) if interview and interview.vacancy_confirm else get_mark_safe(0)

    def sob7_student_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 6:
            qs = obj.interviews.all().order_by('id')
            interview = qs[6] if qs.count() > 6 else None
        return get_mark_safe(1) if interview and interview.student_confirm else get_mark_safe(0)

    def sob7_holidays_period(self, obj, xls=False):
        return f'{obj.summer_holidays_start.strftime("%d.%m.%y")}-{obj.summer_holidays_end.strftime("%d.%m.%y")}' if obj.summer_holidays_start and obj.summer_holidays_end else '-'

    def sob8_company_name(self, obj, xls=False):
        interview = None
        if obj._interview_count > 7:
            qs = obj.interviews.all().order_by('id')
            interview = qs[7] if qs.count() > 7 else None
        return interview.company.name if interview else '-'

    def sob8_position(self, obj, xls=False):
        interview = None
        if obj._interview_count > 7:
            qs = obj.interviews.all().order_by('id')
            interview = qs[7] if qs.count() > 7 else None
        return interview.vacancy.name if interview else '-'

    def sob8_invited_status(self, obj, xls=False):
        if obj._interview_count > 7:
            qs = obj.interviews.all().order_by('id')
            interview = qs[7] if qs.count() > 7 else None
            if interview and interview.invited_status == 'not_invited':
                return get_mark_safe(0)
            elif interview and interview.invited_status == 'doubtful':
                return get_mark_safe(3)
            elif interview and interview.invited_status == 'invited':
                return get_mark_safe(1)
            elif interview and interview.invited_status == 'invited_twice':
                return get_mark_safe(2)
        return get_mark_safe(0)

    def sob8_appointment_date(self, obj, xls=False):
        interview = None
        if obj._interview_count > 7:
            qs = obj.interviews.all().order_by('id')
            interview = qs[7] if qs.count() > 7 else None
        return interview.appointment_date.strftime('%d.%m.%y %H:%M') if interview and interview.appointment_date else '-'

    def sob8_vacancy_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 7:
            qs = obj.interviews.all().order_by('id')
            interview = qs[7] if qs.count() > 7 else None
        return get_mark_safe(1) if interview and interview.vacancy_confirm else get_mark_safe(0)

    def sob8_student_confirm(self, obj, xls=False):
        interview = None
        if obj._interview_count > 7:
            qs = obj.interviews.all().order_by('id')
            interview = qs[7] if qs.count() > 7 else None
        return get_mark_safe(1) if interview and interview.student_confirm else get_mark_safe(0)

    def sob8_holidays_period(self, obj, xls=False):
        return f'{obj.summer_holidays_start.strftime("%d.%m.%y")}-{obj.summer_holidays_end.strftime("%d.%m.%y")}' if obj.summer_holidays_start and obj.summer_holidays_end else '-'

    def payment(self, obj, xls=False):
        return obj.paid_percent
    
    def nvks_custom(self, obj):
        return mark_safe(f'<strong style="color:red; font-size:1.5rem">НВКС</strong>') if obj.nvks else ''

    def export_xls(self, request):
        import xlwt
        from django.utils.safestring import SafeText

        queryset = self.get_queryset(request=request).prefetch_related('interviews').order_by('last_name', 'first_name')

        # filter by search functionality
        search_term = request.GET.get('q')

        if search_term:
            queryset, use_distinct = self.get_search_results(request, queryset, search_term)

        gender = request.GET.get('gender__exact')

        if gender:
            queryset = queryset.filter(gender=gender)

        university = request.GET.get('university__id__exact')

        if university and university.isdigit():
            queryset = queryset.filter(university__id=int(university))

        faculty = request.GET.get('faculty__id__exact')

        if faculty and faculty.isdigit():
            queryset = queryset.filter(faculty__id=int(faculty))

        direction = request.GET.get('direction')

        if direction and direction in ['nord', 'sud']:
            queryset = queryset.filter(direction__exact=direction)

        year = request.GET.get('year__exact')

        if year and year.isdigit():
            queryset = queryset.filter(year=int(year))

        hol_strt1 = request.GET.get('summer_holidays_start__range__gte')
        hol_strt2 = request.GET.get('summer_holidays_start__range__lte')

        if hol_strt1 and re.match('\d{2}.\d{2}.\d{4}', hol_strt1):
            hol_strt1 = '-'.join(hol_strt1.split('.')[::-1])
            queryset = queryset.filter(summer_holidays_start__gte=hol_strt1)

        if hol_strt2 and re.match('\d{2}.\d{2}.\d{4}', hol_strt2):
            hol_strt2 = '-'.join(hol_strt2.split('.')[::-1])
            queryset = queryset.filter(summer_holidays_start__lte=hol_strt2)

        hol_fnsh1 = request.GET.get('summer_holidays_end__range__gte')
        hol_fnsh2 = request.GET.get('summer_holidays_end__range__lte')

        if hol_fnsh1 and re.match('\d{2}.\d{2}.\d{4}', hol_fnsh1):
            hol_fnsh1 = '-'.join(hol_fnsh1.split('.')[::-1])
            queryset = queryset.filter(summer_holidays_end__gte=hol_fnsh1)

        if hol_fnsh2 and re.match('\d{2}.\d{2}.\d{4}', hol_fnsh2):
            hol_fnsh2 = '-'.join(hol_fnsh2.split('.')[::-1])
            queryset = queryset.filter(summer_holidays_end__lte=hol_fnsh2)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Профили")

        row_num = 0

        columns = [
            'Имя',
            'Заметка',
            'Комментарий',
            'День рождения',
            'Номер загранпаспорта',
            'Дата окончания загранпаспорта',
            'Дата термина посольство',
            'Время термина посольство',
            'Номер ID',
            'Пол',
            'Дата начала каникул',
            'Дата окончания каникул',
            'Университет',
            'Факультет',
            'Курс',
            'Номер',
            'Уровень',
            'Курсы',

            'С1 Компания',
            'С1 Вакансия',
            'С1 Приглашен',
            'С1 Дата приглашения',
            'С1 Прошел на вакансию',
            'С1 Подтверждение студента',
            'С1 Дата каникул',

            'С2 Компания',
            'С2 Вакансия',
            'С2 Приглашен',
            'С2 Дата приглашения',
            'С2 Прошел на вакансию',
            'С2 Подтверждение студента',
            'С2 Дата каникул',

            'С3 Компания',
            'С3 Вакансия',
            'С3 Приглашен',
            'С3 Дата приглашения',
            'С3 Прошел на вакансию',
            'С3 Подтверждение студента',
            'С3 Дата каникул',

            'С4 Компания',
            'С4 Вакансия',
            'С4 Приглашен',
            'С4 Дата приглашения',
            'С4 Прошел на вакансию',
            'С4 Подтверждение студента',
            'С4 Дата каникул',

            'С5 Компания',
            'С5 Вакансия',
            'С5 Приглашен',
            'С5 Дата приглашения',
            'С5 Прошел на вакансию',
            'С5 Подтверждение студента',
            'С5 Дата каникул',

            'С6 Компания',
            'С6 Вакансия',
            'С6 Приглашен',
            'С6 Дата приглашения',
            'С6 Прошел на вакансию',
            'С6 Подтверждение студента',
            'С6 Дата каникул',

            'С7 Компания',
            'С7 Вакансия',
            'С7 Приглашен',
            'С7 Дата приглашения',
            'С7 Прошел на вакансию',
            'С7 Подтверждение студента',
            'С7 Дата каникул',

            'С8 Компания',
            'С8 Вакансия',
            'С8 Приглашен',
            'С8 Дата приглашения',
            'С8 Прошел на вакансию',
            'С8 Подтверждение студента',
            'С8 Дата каникул',
        ]

        fields = [
            'full_name_reverse',
            'note',
            'comment',
            'bday',
            'zagranpassport_number_id',
            'zagranpassport_end_time',
            'termin_date',
            'termin_time',
            'passport_number_id',
            'gender',
            'summer_holidays_start',
            'summer_holidays_end',
            'university',
            'faculty',
            'year',
            'phone',
            'level',
            'courses_info',
        ]

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
            # ws.col(col_num).width = columns[col_num][1]

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1

        for obj in queryset:
            row_num += 1
            row = []
            for field in fields:
                if hasattr(obj, field):
                    if field == 'bday':
                        value = obj.bday.strftime('%d.%m.%Y') if obj.bday else '-'
                    elif field == 'gender':
                        value = obj.get_gender_display() if obj.gender else '-'
                    elif field == 'summer_holidays_start':
                        value = obj.summer_holidays_start.strftime('%d.%m.%Y') if obj.summer_holidays_start else '-'
                    elif field == 'summer_holidays_end':
                        value = obj.summer_holidays_end.strftime('%d.%m.%Y') if obj.summer_holidays_end else '-'
                    elif field == 'zagranpassport_end_time':
                        value = obj.zagranpassport_end_time.strftime('%d.%m.%Y') if obj.zagranpassport_end_time else '-'
                    else:
                        value = getattr(obj, field)
                    if type(value) == SafeText:
                        raw = value.split('/')
                        if raw[0] == '<img src="':
                            status = raw[4].split('.svg')[0]
                            if status == 'non_flag':
                                value = 'x'
                            elif status == 'single_flag':
                                value = '✓'
                            elif status == 'double_flag':
                                value = '✓✓'
                            else:
                                value = '?'
                    if type(value) != int or type(value) != float or not value:
                        value = str(value)
                        if value == 'None':
                            value = '-'
                    row.append(value)
                else:
                    value = getattr(self, field)(obj, True)
                    if type(value) == SafeText:
                        raw = value.split('/')
                        if raw[0] == '<img src="':
                            status = raw[4].split('.svg')[0]
                            if status == 'non_flag':
                                value = 'x'
                            elif status == 'single_flag':
                                value = '✓'
                            elif status == 'double_flag':
                                value = '✓✓'
                            else:
                                value = '?'
                    row.append(value)

            for interview in obj.interviews.order_by('id'):
                company_name = interview.company.name if interview.company else '-'
                row.append(company_name)

                vacancy_name = interview.vacancy.name if interview.vacancy else '-'
                row.append(vacancy_name)

                row.append(interview.get_invited_status_display())
                row.append(interview.appointment_date.strftime('%d.%m.%y %H:%M') if interview.appointment_date else '-')
                row.append('V' if interview.vacancy_confirm else 'X')
                row.append('V' if interview.student_confirm else 'X')
                row.append(f'{obj.summer_holidays_start.strftime("%d.%m.%y")}-{obj.summer_holidays_end.strftime("%d.%m.%y")}'
                           if obj.summer_holidays_start and obj.summer_holidays_end else '-')

            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response


    export_xls.short_description = u"Export XLS"

    whatsapp_link.short_description = mark_safe(f'<img src="/static/images/icons/whatsapp.svg" width="18" height="18" />')
    full_name_reverse.short_description = 'Имя'
    note_form.short_description = 'Заметка'
    comment_form.short_description = 'Коммент.'
    phone.short_description = 'Тел.'
    termin_date.short_description = 'Термин(д)'
    termin_time.short_description = 'Термин(вр)'
    passport_number_id.short_description = 'номер ID'

    sob1_company_name.short_description = 'Компания С1'
    sob1_position.short_description = 'Вакансия С1'
    sob1_invited_status.short_description = 'Пригл. С1'
    sob1_appointment_date.short_description = 'Пригл(дата). С1'
    sob1_vacancy_confirm.short_description = 'Прошел С1'
    sob1_student_confirm.short_description = 'Подтв. студента С1'
    sob1_holidays_period.short_description = 'Каникулы С1'

    sob2_company_name.short_description = 'Компания С2'
    sob2_position.short_description = 'Вакансия С2'
    sob2_invited_status.short_description = 'Пригл. С2'
    sob2_appointment_date.short_description = 'Пригл(дата). С2'
    sob2_vacancy_confirm.short_description = 'Прошел С2'
    sob2_student_confirm.short_description = 'Подтв. студента С2'
    sob2_holidays_period.short_description = 'Каникулы С2'

    sob3_company_name.short_description = 'Компания С3'
    sob3_position.short_description = 'Вакансия С3'
    sob3_invited_status.short_description = 'Пригл. С3'
    sob3_appointment_date.short_description = 'Пригл(дата). С3'
    sob3_vacancy_confirm.short_description = 'Прошел С3'
    sob3_student_confirm.short_description = 'Подтв. студента С3'
    sob3_holidays_period.short_description = 'Каникулы С3'

    sob4_company_name.short_description = 'Компания С4'
    sob4_position.short_description = 'Вакансия С4'
    sob4_invited_status.short_description = 'Пригл. С4'
    sob4_appointment_date.short_description = 'Пригл(дата). С4'
    sob4_vacancy_confirm.short_description = 'Прошел С4'
    sob4_student_confirm.short_description = 'Подтв. студента С4'
    sob4_holidays_period.short_description = 'Каникулы С4'

    sob5_company_name.short_description = 'Компания С5'
    sob5_position.short_description = 'Вакансия С5'
    sob5_invited_status.short_description = 'Пригл. С5'
    sob5_appointment_date.short_description = 'Пригл(дата). С5'
    sob5_vacancy_confirm.short_description = 'Прошел С5'
    sob5_student_confirm.short_description = 'Подтв. студента С5'
    sob5_holidays_period.short_description = 'Каникулы С5'

    sob6_company_name.short_description = 'Компания С6'
    sob6_position.short_description = 'Вакансия С6'
    sob6_invited_status.short_description = 'Пригл. С6'
    sob6_appointment_date.short_description = 'Пригл(дата). С6'
    sob6_vacancy_confirm.short_description = 'Прошел С6'
    sob6_student_confirm.short_description = 'Подтв. студента С6'
    sob6_holidays_period.short_description = 'Каникулы С6'

    sob7_company_name.short_description = 'Компания С7'
    sob7_position.short_description = 'Вакансия С7'
    sob7_invited_status.short_description = 'Пригл. С7'
    sob7_appointment_date.short_description = 'Пригл(дата). С7'
    sob7_vacancy_confirm.short_description = 'Прошел С7'
    sob7_student_confirm.short_description = 'Подтв. студента С7'
    sob7_holidays_period.short_description = 'Каникулы С7'

    sob8_company_name.short_description = 'Компания С8'
    sob8_position.short_description = 'Вакансия С8'
    sob8_invited_status.short_description = 'Пригл. С8'
    sob8_appointment_date.short_description = 'Пригл(дата). С8'
    sob8_vacancy_confirm.short_description = 'Прошел С8'
    sob8_student_confirm.short_description = 'Подтв. студента С8'
    sob8_holidays_period.short_description = 'Каникулы С8'
    payment.short_description = 'Оплата (в процентах)'
    zagranpassport_number_id.short_description = 'Номер заграна'
    zagranpassport_end_time_admin.short_description = 'Оконч. загр.'
    nvks_custom.short_description = 'НВКС'
