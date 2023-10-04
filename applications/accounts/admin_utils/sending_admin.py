import re
from distutils import util

from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils.safestring import mark_safe, SafeText

from applications.accounts.models import Profile
from .inlines import NotificationsInline, InterviewInline
from applications.accounts import filters
from applications.accounts.filters import CustomDateFilter
from applications.accounts.utils import get_mark_safe


class ProfileInSendingAdmin(admin.ModelAdmin):
    inlines = [
        NotificationsInline,
        InterviewInline,
    ]

    fields = [
        'first_name', 'last_name', 'bday', 'passport_number', 'zagranpassport_number', 'zagranpassport_end_time',
        'embassy_visametric', 'termin', 'university', 'faculty', 'year', 'zagranpassport_copy', 'full_sum',
        'start_vise_date', 'end_vise_date', 'flight_date', 'arrival_date', 'destination_date', 'arrival_city',
        'arrival_airport', 'arrival_place', 'marshrut', 'immatrikulation_received', 'domkom_document', 'bilet_document',
        'akt_trainings', 'akt_iwex', 'receipt_flight', 'consultant_before_flight',
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
        'work_period',
        'visa_period',
        'employer',
        'flight_date_custom',
        'arrival_date_custom',
        'arrival_city_custom',
        'arrival_airport_custom',
        'destination_custom',
        'destination_date_custom',
        'marshrut_custom',
        'immat_custom',
        'domkom_custom',
        'bilet_custom',
        'work_contract_custom',
        'bank_data_custom',
        'raspiska_pered_otezdom',
        'akt_trainings_custom',
        'akt_iwex_custom',
        'debt_custom',
        'consult_date_custom',
        'consultant_custom',
    ]

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
        filters.DirectionFilter,
        filters.Marshrut,
        filters.ImatGiven,
        filters.Domkom,
        filters.BiletSending,
        filters.AktTrainings,
        filters.AktIwex,
        'employer',
        ('work_from', CustomDateFilter),
        ('work_to', CustomDateFilter),
        ('start_vise_date', CustomDateFilter),
        ('end_vise_date', CustomDateFilter),
        ('flight_date', CustomDateFilter),
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
        extra_context['table_classname'] = 'vacancy'
        return super(ProfileInSendingAdmin, self).changelist_view(request, extra_context=extra_context)

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

    def consult_date_custom(self, obj):
        return obj.consult_date.strftime('%d.%m.%Y') if obj.consult_date else '-'

    def consultant_custom(self, obj):
        return obj.consultant if obj.consultant else '-'

    def debt_custom(self, obj):
        return obj.lost_sum

    def akt_trainings_custom(self, obj):
        return get_mark_safe(1) if obj.akt_trainings else get_mark_safe(0)

    def akt_iwex_custom(self, obj):
        return get_mark_safe(1) if obj.akt_iwex else get_mark_safe(0)

    def marshrut_custom(self, obj):
        if obj.marshrut == 'created':
            return get_mark_safe(1)
        elif obj.marshrut == 'received':
            return get_mark_safe(2)
        elif obj.marshrut == 'doubtful':
            return get_mark_safe(3)
        return get_mark_safe(0)

    def domkom_custom(self, obj):
        if obj.domkom_document == 'brought':
            return get_mark_safe(1)
        elif obj.domkom_document == 'sent':
            return get_mark_safe(2)
        elif obj.domkom_document == 'not_given':
            return get_mark_safe(3)
        return get_mark_safe(0)

    def bilet_custom(self, obj):
        if obj.bilet_document == 'brought':
            return get_mark_safe(1)
        elif obj.bilet_document == 'sent':
            return get_mark_safe(2)
        elif obj.bilet_document == 'not_given':
            return get_mark_safe(3)
        return get_mark_safe(0)

    def bank_data_custom(self, obj):
        if obj.bank_details and not obj.bank_details_confirm:
            return get_mark_safe(3)
        elif obj.bank_details and obj.bank_details_confirm:
            return get_mark_safe(1)
        elif obj.bank_details and obj.bank_details_confirm and obj.bank_details_paper_confirm:
            return get_mark_safe(2)
        return get_mark_safe(0)

    def raspiska_pered_otezdom(self, obj):
        return get_mark_safe(1) if obj.receipt_flight else get_mark_safe(0)

    def work_contract_custom(self, obj):
        return get_mark_safe(1) if obj.work_contract_paper_confirm else get_mark_safe(0)

    def immat_custom(self, obj):
        return get_mark_safe(1) if obj.immatrikulation_received else get_mark_safe(0)

    def flight_date_custom(self, obj):
        return obj.flight_date.strftime('%d.%m.%Y %H:%M') if obj.flight_date else '-'

    def arrival_date_custom(self, obj):
        return obj.arrival_date.strftime('%d.%m.%Y %H:%M') if obj.arrival_date else '-'

    def arrival_city_custom(self, obj):
        return obj.arrival_city if obj.arrival_city else '-'

    def arrival_airport_custom(self, obj):
        return obj.arrival_airport if obj.arrival_airport else '-'

    def destination_custom(self, obj):
        return obj.arrival_place if obj.arrival_place else '-'

    def destination_date_custom(self, obj):
        return obj.destination_date.strftime('%d.%m.%Y %H:%M') if obj.destination_date else '-'

    def nvks_custom(self, obj):
        return mark_safe(f'<strong style="color:red; font-size:1.5rem">НВКС</strong>') if obj.nvks else ''

    def whatsapp_link(self, obj):
        return mark_safe(
            f'<a href="https://api.whatsapp.com/send?phone={obj.user.whatsapp_phone}" target="_blank" title="Написать на {obj.user.whatsapp_phone}"><img src="/static/images/icons/whatsapp.svg" width="18" height="18" /></a>')

    def full_name_reverse(self, obj):
        return mark_safe(
            f'<a href="/admin/accounts/profileinsending/{obj.id}/change?next=/admin/accounts/profileinsending/" title="{obj.full_name_reverse}">{obj.full_name_reverse}</a>')

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

    def phone(self, obj):
        return obj.user.phone

    def employer(self, obj):
        return obj.company_name if obj.company_name else '-'

    def work_period(self, obj):
        return f'{obj.work_from.strftime("%d.%m.%y")}-{obj.work_to.strftime("%d.%m.%y")}' if obj.work_from and obj.work_to else '-'

    def visa_period(self, obj):
        return f'{obj.start_vise_date.strftime("%d.%m.%y")}-{obj.end_vise_date.strftime("%d.%m.%y")}' if obj.start_vise_date and obj.end_vise_date else '-'

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

        if faculty and faculty.isdigit():
            queryset = queryset.filter(faculty__id=int(faculty))

        course = request.GET.get('year__exact')

        direction = request.GET.get('direction')

        if direction and direction in ['nord', 'sud']:
            queryset = queryset.filter(direction__exact=direction)

        if course and course.isdigit():
            queryset = queryset.filter(year=int(course))

        marshrut = request.GET.get('marshrut')

        if marshrut and marshrut in ['not_exist', 'doubtful', 'created', 'received']:
            queryset = queryset.filter(marshrut=marshrut)

        imat = request.GET.get('immatrikulation_received')

        if imat and imat in ['yes', 'no']:
            queryset = queryset.filter(immatrikulation_received=util.strtobool(imat))

        spravka = request.GET.get('domkom_document')

        if spravka and spravka in ['not_exist', 'brought', 'sent', 'not_given']:
            queryset = queryset.filter(domkom_document=spravka)

        bilet = request.GET.get('bilet_document')

        if bilet and bilet in ['not_exist', 'brought', 'sent', 'not_given']:
            queryset = queryset.filter(bilet_document=bilet)

        train = request.GET.get('akt_trainings')

        if train and train in ['yes', 'no']:
            queryset = queryset.filter(akt_trainings=util.strtobool(train))

        akt_iwex = request.GET.get('akt_iwex')

        if akt_iwex and akt_iwex in ['yes', 'no']:
            queryset = queryset.filter(akt_iwex=util.strtobool(akt_iwex))

        wrk_strt = request.GET.get('work_from__range__gte')
        wrk_fnsh = request.GET.get('work_from__range__lte')

        if wrk_strt and re.match('\d{2}.\d{2}.\d{4}', wrk_strt):
            wrk_strt = '-'.join(wrk_strt.split('.')[::-1])
            queryset = queryset.filter(work_from__gte=wrk_strt)

        if wrk_fnsh and re.match('\d{2}.\d{2}.\d{4}', wrk_fnsh):
            wrk_fnsh = '-'.join(wrk_fnsh.split('.')[::-1])
            queryset = queryset.filter(wortk_from__lte=wrk_fnsh)

        wrk_to_strt = request.GET.get('work_to_range__gte')
        wrk_to_fnsh = request.GET.get('work_to_range__lte')

        if wrk_to_strt and re.match('\d{2}.\d{2}.\d{4}', wrk_to_strt):
            wrk_to_strt = '-'.join(wrk_to_strt.split('.')[::-1])
            queryset = queryset.filter(work_to__gte=wrk_to_strt)

        if wrk_to_fnsh and re.match('\d{2}.\d{2}.\d{4}', wrk_to_fnsh):
            wrk_to_fnsh = '-'.join(wrk_to_fnsh.split('.')[::-1])
            queryset = queryset.filter(work_to__lte=wrk_to_fnsh)

        strt_vise_strt = request.GET.get('start_vise_date__range__gte')
        strt_vise_fnsh = request.GET.get('start_vise_date__range__lte')

        if strt_vise_strt and re.match('\d{2}.\d{2}.\d{4}', strt_vise_strt):
            strt_vise_strt = '-'.join(strt_vise_strt.split('.')[::-1])
            queryset = queryset.filter(start_vise_date__gte = strt_vise_strt)

        if strt_vise_fnsh and re.match('\d{2}.\d{2}.\d{4}', strt_vise_fnsh):
            strt_vise_fnsh = '-'.join(strt_vise_fnsh.split('.')[::-1])
            queryset = queryset.filter(start_vise_date__lte = strt_vise_fnsh)

        end_vise_strt = request.GET.get('end_vise_date__range__gte')
        end_vise_fnsh = request.GET.get('end_vise_date__range__lte')

        if end_vise_strt and re.match('\d{2}.\d{2}.\d{4}', end_vise_strt):
            end_vise_strt = '-'.join(end_vise_strt.split('.')[::-1])
            queryset = queryset.filter(end_vise_date__gte=end_vise_strt)
        if end_vise_fnsh and re.match('\d{2}.\d{2}.\d{4}', end_vise_fnsh):
            end_vise_fnsh = '-'.join(end_vise_fnsh.split('.')[::-1])
            queryset = queryset.filter(end_vise_date__lte=end_vise_fnsh)

        flight_date_strt = request.GET.get('flight_date__range__gte')
        flight_date_fnsh = request.GET.get('flight_date__range__lte')

        if flight_date_strt and re.match('\d{2}.\d{2}.\d{4}', flight_date_strt):
            flight_date_strt = '-'.join(flight_date_strt.split('.')[::-1])
            queryset = queryset.filter(flight_date__gte=flight_date_strt)

        if flight_date_fnsh and re.match('\d{2}.\d{2}.\d{4}', flight_date_fnsh):
            flight_date_fnsh = '-'.join(flight_date_fnsh.split('.')[::-1])
            queryset = queryset.filter(flight_date__lte=flight_date_fnsh)

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
            'work_period',
            'visa_period',
            'employer',
            'flight_date_custom',
            'arrival_date_custom',
            'arrival_city_custom',
            'arrival_airport_custom',
            'destination_custom',
            'destination_date_custom',
            'marshrut_custom',
            'immat_custom',
            'domkom_custom',
            'bilet_custom',
            'work_contract_custom',
            'bank_data_custom',
            'raspiska_pered_otezdom',
            'akt_trainings_custom',
            'akt_iwex_custom',
            'debt_custom',
            'consult_date_custom',
            'consultant_custom',
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

    whatsapp_link.short_description = mark_safe(
        f'<img src="/static/images/icons/whatsapp.svg" width="18" height="18" />')
    full_name_reverse.short_description = 'Имя'
    note_form.short_description = 'Заметка'
    comment_form.short_description = 'Коммент.'
    phone.short_description = 'Тел.'
    employer.short_description = 'Работодатель'
    work_period.short_description = 'Период работы'
    visa_period.short_description = 'Период визы'
    flight_date_custom.short_description = 'Вылет в Гер.'
    arrival_date_custom.short_description = 'Прилет в Гер.'
    arrival_city_custom.short_description = 'Город'
    arrival_airport_custom.short_description = 'Аэропорт'
    destination_custom.short_description = 'Пункт назн.'
    destination_date_custom.short_description = 'Пункт назн.(д)'
    marshrut_custom.short_description = 'Маршрут'
    immat_custom.short_description = 'Immat'
    domkom_custom.short_description = 'Домком'
    bilet_custom.short_description = 'Билет'
    work_contract_custom.short_description = 'Раб. дог.'
    bank_data_custom.short_description = 'Рекв. банка'
    raspiska_pered_otezdom.short_description = 'Расписка инструктаж'
    akt_trainings_custom.short_description = 'Акт по трен.'
    akt_iwex_custom.short_description = 'Акт IWEX'
    debt_custom.short_description = 'Долг'
    consult_date_custom.short_description = 'Дата конс.'
    consultant_custom.short_description = 'Консультант'
    zagranpassport_number_id.short_description = 'Номер заграна'
    zagranpassport_end_time_admin.short_description = 'Оконч. загр.'
    termin_date.short_description = 'Термин(д)'
    termin_time.short_description = 'Термин(вр)'
    nvks_custom.short_description = 'НВКС'
