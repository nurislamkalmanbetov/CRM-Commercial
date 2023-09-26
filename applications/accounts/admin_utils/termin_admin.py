import re

from django.contrib.admin.helpers import ActionForm
from django.contrib import admin
from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.safestring import mark_safe, SafeText

from applications.accounts.forms import ManagersListForm
from applications.accounts.models import Profile, Staff
from applications.accounts import filters
from applications.accounts.filters import CustomDateFilter
from django.contrib import messages


class TerminActionForm(ActionForm):
    manager = forms.ModelChoiceField(queryset=Staff.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manager'].empty_label = None
        self.fields['manager'].label = 'Менеджер'


class ProfileInTerminAdmin(admin.ModelAdmin):

    actions = ['set_manager', ]

    action_form = TerminActionForm

    fields = [
        'first_name', 'last_name', 'nationality', 'bday', 'passport_number', 'zagranpassport_number',
        'zagranpassport_end_time', 'zagranpassport_copy',
        'new_email', 'has_termin', 'termin', 'pnr_code', 'termin_scan',
        'note', 'comment', 'director_manager',
    ]

    list_display = [
        'whatsapp_link',
        'note_form',
        'comment_form',
        'profile_details',
        'first_name_custom',
        'last_name_custom',
        'nationality_custom',
        'bday_custom',
        'zagranpassport_number_id_custom',
        'zagranpassport_end_time_admin_custom',
        'new_email_custom',
        'phone_custom',
        'termin_date_custom',
        'termin_time_custom',
        'pnr_code_custom',
        'level',
        'courses_info',
        'termin_scan',
        'director_manager',
    ]

    ordering = ['-in_review', '-termin', '-work_invitation_date', '-summer_holidays_start']

    search_fields = [
        'first_name',
        'last_name',
        'user__phone',
        'passport_number',
        'zagranpassport_number',
    ]

    list_filter = [
        'university',
        'faculty',
        'year',
        'director_manager',
        filters.DirectionFilter,
        ('summer_holidays_start', CustomDateFilter),
        ('summer_holidays_end', CustomDateFilter),
        ('termin', CustomDateFilter),
    ]

    change_list_template = 'admin/accounts/change_list_termin.html'

    class Media:
        css = {
            'all': ('admin/css/changelists_custom.css', )
        }
        js = ('admin/js/termin.js', )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def set_manager(self, request, queryset):
        manager = request.POST.get('manager')
        if manager:
            queryset.update(director_manager=manager)
            messages.add_message(request, messages.SUCCESS, 'Пользователи были успешно сохранены')
        else:
            messages.add_message(request, messages.ERROR, 'Выберите менеджера!')

    set_manager.short_description = 'Выбрать менеджера'

    def changelist_view(self, request, extra_context=None):

        if request.GET.get('get_xls', None):
            return self.export_xls(request)

        extra_context = extra_context or {}
        extra_context['table_classname'] = 'termin'
        return super(ProfileInTerminAdmin, self).changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        profile = get_object_or_404(Profile, pk=object_id)
        if profile and profile.photo:
            extra_context['photo_url'] = profile.photo.url
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def profile_details(self, obj):
        return mark_safe(f'<a href="/admin/accounts/profileintermin/{obj.id}/change?next=/admin/accounts/profileintermin/" title="Детали профиля">Детали профиля</a>')

    def first_name_custom(self, obj):
        return mark_safe(
            f"<button class=\"copy_button\">{obj.first_name}</button>") if obj.first_name else '-'

    def last_name_custom(self, obj):
        return mark_safe(
            f"<button class=\"copy_button\">{obj.last_name}</button>") if obj.last_name else '-'

    def termin_date_custom(self, obj):
        return mark_safe(f"<button class=\"copy_button\">{obj.termin.strftime('%d.%m.%y')}</button>") if obj.termin else '-'
    
    def bday_custom(self, obj):
        return mark_safe(f"<button class=\"copy_button\">{obj.bday.strftime('%d.%m.%Y')}</button>") if obj.bday else '-'

    def termin_time_custom(self, obj):
        return mark_safe(f"<button class=\"copy_button\">{obj.termin.strftime('%H:%M')}</button>") if obj.termin else '-'

    def zagranpassport_number_id_custom(self, obj, xls=False):
        return mark_safe(f"<button class=\"copy_button\">{obj.zagranpassport_number}</button>") if obj.zagranpassport_number else '-'

    def zagranpassport_end_time_admin_custom(self, obj, xls=False):
        return mark_safe(f"<button class=\"copy_button\">{obj.zagranpassport_end_time.strftime('%d.%m.%Y')}</button>") if obj.zagranpassport_end_time else '-'

    def nationality_custom(self, obj):
        return mark_safe(f"<button class=\"copy_button\">{obj.nationality}</button>") if obj.nationality else '-'

    def whatsapp_link(self, obj):
        return mark_safe(
            f'<a href="https://api.whatsapp.com/send?phone={obj.user.whatsapp_phone}" target="_blank" title="Написать на {obj.user.whatsapp_phone}"><img src="/static/images/icons/whatsapp.svg" width="18" height="18" /></a>')

    def full_name_reverse(self, obj):
        return mark_safe(f"<button class=\"copy_button\">{obj.full_name_reverse}</button>") if obj.full_name_reverse else '-'

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

    def phone_custom(self, obj):
        return mark_safe(f"<button class=\"copy_button\">{obj.user.phone}</button>") if obj.user.phone else '-'

    def new_email_custom(self, obj):
        return mark_safe(f"<button class=\"copy_button\">{obj.new_email}</button>") if obj.new_email else '-'

    def nvks_custom(self, obj):
        return mark_safe(f'<strong style="color:red; font-size:1.5rem">НВКС</strong>') if obj.nvks else ''

    def pnr_code_custom(self, obj):
        return mark_safe(f"<button class=\"copy_button\">{obj.pnr_code}</button>") if obj.pnr_code else '-'

    def export_xls(self, request):
        import xlwt

        queryset = self.get_queryset(request=request).order_by('last_name', 'first_name')

        # filter by search functionality
        search_term = request.GET.get('q')

        if search_term:
            queryset, use_distinct = self.get_search_results(request, queryset, search_term)

        university = request.GET.get('university__id__exact')

        if university and university.isdigit():
            queryset = queryset.filter(university__id=int(university))

        faculty = request.GET.get('faculty__id__exact')

        director_manager = request.GET.get('director_manager__id__exact')

        if director_manager and director_manager.is_digit():
            queryset = queryset.filter(director_manager__id=int(director_manager))

        if faculty and faculty.isdigit():
            queryset = queryset.filter(faculty__id=int(faculty))
        
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
        
        termin_start = request.GET.get('termin__range__gte')
        termin_finish = request.GET.get('termin__range__lte')

        if termin_start and re.match('\d{2}.\d{2}.\d{4}', termin_start):
            termin_start = '-'.join(termin_start.split('.')[::-1])
            queryset = queryset.filter(termin__range__gte=termin_start)

        if termin_finish and re.match('\d{2}.\d{2}.\d{4}', termin_finish):
            termin_finish = '-'.join(termin_finish.split('.')[::-1])
            queryset = queryset.filter(termin__range__lte=termin_finish)

        direction = request.GET.get('direction')

        if direction and direction in ['nord', 'sud']:
            
            queryset = queryset.filter(direction__exact=direction)
        
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Профили")

        row_num = 0

        columns = [
            'Имя',
            'Фамилия',
            'Гражданство',
            'День рождения',
            'Номер загранпаспорта',
            'Дата окончания загранпаспорта',
            'Новая почта',
            'Номер',
            'Дата термина посольство',
            'Время термина посольство',
            'PNR-код',
            'Консультант'
        ]

        fields = [
            'first_name',
            'last_name',
            'nationality',
            'bday',
            'zagranpassport_number',
            'zagranpassport_end_time',
            'new_email',
            'phone',
            'termin_date',
            'termin_time',
            'pnr_code',
            'director_manager',
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
                    elif field == 'zagranpassport_end_time':
                        value = obj.zagranpassport_end_time.strftime('%d.%m.%Y') if obj.zagranpassport_end_time else '-'
                    else:
                        value = getattr(obj, field)

                    if type(value) != int or type(value) != float or not value:
                        value = str(value)
                    row.append(value)
                elif field == 'termin_date':
                    value = obj.termin.strftime('%d.%m.%Y') if obj.termin else '-'
                    row.append(value)
                elif field == 'termin_time':
                    value = obj.termin.strftime('%H:%M') if obj.termin else '-'
                    row.append(value)
                elif field == 'phone':
                    value = obj.user.phone
                    row.append(value)
                else:
                    value = getattr(self, field)(obj)
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
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

    export_xls.short_description = u"Export XLS"

    whatsapp_link.short_description = mark_safe(f'<img src="/static/images/icons/whatsapp.svg" width="18" height="18" />')
    profile_details.short_description = 'Детали профиля'
    full_name_reverse.short_description = 'Имя'
    bday_custom.short_description = 'Дата рождения'
    note_form.short_description = 'Заметка'
    comment_form.short_description = 'Коммент.'
    phone_custom.short_description = 'Тел.'
    termin_date_custom.short_description = 'Термин(д)'
    termin_time_custom.short_description = 'Термин(вр)'
    zagranpassport_number_id_custom.short_description = 'Номер заграна'
    zagranpassport_end_time_admin_custom.short_description = 'Оконч. загр.'
    nvks_custom.short_description = 'НВКС'
    nationality_custom.short_description = 'Гражданство'
    new_email_custom.short_description = 'Новая почта'
    pnr_code_custom.short_description = 'PNR код'
    first_name_custom.short_description = 'Имя'
    last_name_custom.short_description = 'Фамилия'
