from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils.safestring import mark_safe, SafeText

from applications.accounts.models import Profile, Bill
from .inlines import NotificationsInline, BillInline
from applications.accounts import filters
from applications.accounts.filters import CustomDateFilter


class ProfileInPaymentAdmin(admin.ModelAdmin):
    inlines = [
        NotificationsInline,
        BillInline,
    ]

    fields = [
        'first_name', 'last_name', 'bday', 'training_sum', 'employment_sum', 'full_sum',
        'passport_number', 'zagranpassport_number', 'zagranpassport_end_time',
        'embassy_visametric', 'termin', 'university', 'faculty', 'year',
    ]

    list_display = [
        'whatsapp_link',
        'full_name_reverse',
        'nvks_custom',
        'note_form',
        'comment_form',
        'university',
        'faculty',
        'year',
        'termin_date',
        'termin_time',
        'zagranpassport_number_id',
        'zagranpassport_end_time_admin',
        'phone',
        'paid_sum',
        'need_to_pay',
        'full_sum',
        'user_consultant',
    ]

    search_fields = [
        'user__email',
        'first_name',
        'last_name',
        'user__phone',
    ]

    list_filter = [
        'university',
        'faculty',
        'year',
        filters.DirectionFilter,
        ('study_start', CustomDateFilter),
        ('study_end', CustomDateFilter)
    ]

    change_list_template = 'admin/accounts/change_list.html'

    class Media:
        css = {
            'all': ('admin/css/changelists_custom.css',)
        }

    def changelist_view(self, request, extra_context=None):
        if request.GET.get('get_xls', None):
            return self.export_xls(request)

        extra_context = extra_context or {}
        extra_context['table_classname'] = 'payment'
        return super(ProfileInPaymentAdmin, self).changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        profile = get_object_or_404(Profile, pk=object_id)
        if profile and profile.photo:
            extra_context['photo_url'] = profile.photo.url
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def termin_date(self, obj):
        return obj.termin.strftime('%d.%m.%y') if obj.termin else '-'

    def termin_time(self, obj):
        return obj.termin.strftime('%H:%M') if obj.termin else '-'

    def zagranpassport_number_id(self, obj, xls=False):
        return obj.zagranpassport_number

    def zagranpassport_end_time_admin(self, obj, xls=False):
        return obj.zagranpassport_end_time

    def whatsapp_link(self, obj):
        return mark_safe(
            f'<a href="https://api.whatsapp.com/send?phone={obj.user.whatsapp_phone}" target="_blank" title="Написать на {obj.user.whatsapp_phone}"><img src="/static/images/icons/whatsapp.svg" width="18" height="18" /></a>')

    def full_name_reverse(self, obj):
        return mark_safe(
            f'<a href="/admin/accounts/profileinpayment/{obj.id}/change?next=/admin/accounts/profileinpayment/" title="{obj.full_name_reverse}">{obj.full_name_reverse}</a>')

    def note_form(self, obj):
        action = '/api/v1/update_note/'
        return mark_safe(   f'''<div class="note_form" data-action="{action}" data-user-id="{obj.id}">
                                    <span class="note_form_text">{obj.note} </span>
                                    <input class="note_form__input" type="text" value="{obj.note}" name="note" />
                                    <button class="note_form__button"><img src="/static/images/icons/save.svg" width="18" height="18" /></button>
                                </div>''')
    
    def comment_form(self, obj):
        action = '/api/v1/update_comment/'
        return mark_safe(   f'''<div class="comment_form" data-action="{action}" data-user-id="{obj.id}">
                                    <span class="note_form_text">{obj.comment} </span>
                                    <input class="comment_form__input" type="text" value="{obj.comment}" name="comment" />
                                    <button class="comment_form__button"><img src="/static/images/icons/save.svg" width="18" height="18" /></button>
                                </div>''')
    
    def nvks_custom(self, obj):
        return mark_safe(f'<strong style="color:red; font-size:1.5rem">НВКС</strong>') if obj.nvks else ''

    def phone(self, obj):
        return obj.user.phone

    def paid_sum(self, obj):
        return obj.paid_sum

    def need_to_pay(self, obj):
        return obj.full_sum - obj.paid_sum if obj.full_sum else 'НЕТ СУММЫ К ОПЛАТЕ'

    def user_consultant(self, obj):
        return obj.consultant

    def export_xls(self, request):
        import xlwt

        queryset = self.get_queryset(request=request).order_by('last_name', 'first_name')

        # filter by search functionality
        search_term = request.GET.get('q')

        if search_term:
            queryset, use_distinct = self.get_search_results(request, queryset, search_term)

        course = request.GET.get('year__exact')

        if course and course.isdigit():
            queryset = queryset.filter(year=int(course))

        faculty = request.GET.get('faculty__id__exact')

        if faculty and faculty.isdigit():
            queryset = queryset.filter(faculty__id=int(faculty))

        university = request.GET.get('university__id__exact')

        if university and university.isdigit():
            queryset = queryset.filter(university__id=int(university))

        direction = request.GET.get('direction')

        if direction and direction in ['nord', 'sud']:
            queryset = queryset.filter(direction__exact=direction)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Профили")

        row_num = 0

        fields = [
            'full_name_reverse',
            'note',
            'comment',
            'termin_date',
            'termin_time',
            'bday',
            'zagranpassport_number_id',
            'zagranpassport_end_time',
            'university',
            'faculty',
            'year',
            'phone',
            'paid_sum',
            'need_to_pay',
            'full_sum',
            'user_consultant',
        ]

        columns = []
        model_fields = [x.name for x in Profile._meta.get_fields()]
        for field in fields:
            if field in model_fields:
                columns.append(Profile._meta.get_field(field).verbose_name)
            else:
                columns.append(getattr(self, field).short_description)

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
    full_name_reverse.short_description = 'Имя'
    note_form.short_description = 'Заметка'
    comment_form.short_description = 'Коммент.'
    phone.short_description = 'Номер'
    paid_sum.short_description = 'Оплатил'
    need_to_pay.short_description = 'Долг'
    user_consultant.short_description = 'Договор с'
    zagranpassport_number_id.short_description = 'Номер заграна'
    zagranpassport_end_time_admin.short_description = 'Оконч. загр.'
    termin_date.short_description = 'Термин(д)'
    termin_time.short_description = 'Термин(вр)'
    nvks_custom.short_description = 'НВКС'

    def save_formset(self, request, form, formset, change):
        if formset.model != Bill:
            return super(ProfileInPaymentAdmin, self).save_formset(request, form, formset, change)
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:
                instance.who_created = request.user
            instance.save()
        formset.save_m2m()
        return formset.save()