from distutils import util

from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import path

from applications.accounts.models import Profile
from .inlines import NotificationsInline, InterviewInline
from applications.accounts.utils import get_mark_safe
from django.utils.safestring import mark_safe, SafeText
from applications.accounts import filters
from ...core.models import EmployerCompany


class ProfileInVacancyAdmin(admin.ModelAdmin):
    inlines = [
        NotificationsInline,
        InterviewInline,
    ]

    readonly_fields = ['payment']

    fields = [
        'first_name', 'last_name', 'access_to_embassy_documents', 'bday', 'passport_number', 'zagranpassport_number', 'zagranpassport_end_time',
        'embassy_visametric', 'termin', 'university', 'faculty', 'year', 'zagranpassport_copy', 'immatrikulation',
        'payment', 'accomodation_type', 'living_condition', 'receipt_paper_confirm', 'employer_confirm_date', 'zav_send_date',
        'work_permit_date', 'work_invitation_date', 'documents_send_date',
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
        'employer',
        'position',
        'work_period',
        'work_city',
        'receipt',
        'employer_confirm',
        'employer_confirm_dt',
        'zav_send_status',
        'zav_send_dt',
        'work_permit_status',
        'work_permit_dt',
        'documents_send_status',
        'documents_send_dt',
        'work_invitation_dt',
        'german_insurance_custom',
        'accomodation_status',
        'accomodation_type',
        'german_work_contract_custom',
        'payment',
    ]

    search_fields = [
        'first_name',
        'last_name',
        'user__phone',
        'passport_number',
        'zagranpassport_number',
        'company_name',
        'position',
    ]

    list_filter = [
        'university',
        'faculty',
        'year',
        'receipt_paper_confirm',
        filters.DirectionFilter,
        ('study_start', filters.CustomDateFilter),
        ('study_end', filters.CustomDateFilter),
        'employer',
    ]

    change_list_template = 'admin/accounts/change_list.html'

    class Media:
        css = {
            'all': ('admin/css/changelists_custom.css',)
        }

        js = ('admin/js/vacancy_admin.js', )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('companies/vacancies/<int:company_id>/', self.admin_site.admin_view(self.vacancy_of_company)),
        ]
        return my_urls + urls

    def vacancy_of_company(self, request, company_id):

        company = EmployerCompany.objects.filter(id=company_id).first()

        if company:
            vacancies = company.vacancies.all()
            vacancies_list = [{'id': vacancy.id, 'name': vacancy.name} for vacancy in vacancies]
            return JsonResponse({'status': 200, 'vacancies': vacancies_list})
        return JsonResponse({'status': 404, 'message': 'no company with such id'})

    def changelist_view(self, request, extra_context=None):

        if request.GET.get('get_xls', None):
            return self.export_xls(request)

        extra_context = extra_context or {}
        extra_context['table_classname'] = 'vacancy'
        return super(ProfileInVacancyAdmin, self).changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        profile = get_object_or_404(Profile, pk=object_id)
        if profile and profile.photo:
            extra_context['photo_url'] = profile.photo.url
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def zagranpassport_number_id(self, obj, xls=False):
        return obj.zagranpassport_number

    def zagranpassport_end_time_admin(self, obj, xls=False):
        return obj.zagranpassport_end_time

    def whatsapp_link(self, obj):
        return mark_safe(
            f'<a href="https://api.whatsapp.com/send?phone={obj.user.whatsapp_phone}" target="_blank" title="Написать на {obj.user.whatsapp_phone}"><img src="/static/images/icons/whatsapp.svg" width="18" height="18" /></a>')

    def full_name_reverse(self, obj):
        return mark_safe(
            f'<a href="/admin/accounts/profileinvacancy/{obj.id}/change?next=/admin/accounts/profileinvacancy/" title="{obj.full_name_reverse}">{obj.full_name_reverse}</a>')

    def note_form(self, obj):
        action = '/api/v1/update_note/'
        return mark_safe(   f'''<div class="note_form" data-action="{action}" data-user-id="{obj.id}">
                                    <span class="note_form_text">{obj.note}</span>
                                    <input class="note_form__input" type="text" value="{obj.note}" name="note" />
                                    <button class="note_form__button"><img src="/static/images/icons/save.svg" width="18" height="18" /></button>
                                </div>''')

    def comment_form(self, obj):
        action = '/api/v1/update_comment/'
        return mark_safe(   f'''<div class="comment_form" data-action="{action}" data-user-id="{obj.id}">
                                    <span class="note_form_text">{obj.comment}</span>
                                    <input class="comment_form__input" type="text" value="{obj.comment}" name="comment" />
                                    <button class="comment_form__button"><img src="/static/images/icons/save.svg" width="18" height="18" /></button>
                                </div>''')

    def phone(self, obj):
        return obj.user.phone

    def termin_date(self, obj):
        return obj.termin.strftime('%d.%m.%y') if obj.termin else '-'

    def termin_time(self, obj):
        return obj.termin.strftime('%H:%M') if obj.termin else '-'

    def employer(self, obj):
        return obj.company_name if obj.company_name else '-'

    def position(self, obj):
        return obj.position if obj.position else '-'

    def work_period(self, obj):
        return f'{obj.work_from.strftime("%d.%m.%y")}-{obj.work_to.strftime("%d.%m.%y")}' if obj.work_from and obj.work_to else '-'

    def work_city(self, obj):
        interview = obj.interviews.filter(student_confirm=True, vacancy_confirm=True).order_by('id').last()
        return interview.city if interview and interview.city else '-'

    def receipt(self, obj):
        return get_mark_safe(1) if obj.receipt_paper_confirm else get_mark_safe(0)

    def employer_confirm(self, obj):
        return get_mark_safe(1) if obj.employer_confirm_date else get_mark_safe(0)

    def employer_confirm_dt(self, obj):
        return obj.employer_confirm_date.strftime('%d.%m.%y') if obj.employer_confirm_date else '-'

    def zav_send_status(self, obj):
        return get_mark_safe(1) if obj.zav_send_date else get_mark_safe(0)

    def zav_send_dt(self, obj):
        return obj.zav_send_date.strftime('%d.%m.%y') if obj.zav_send_date else '-'

    def work_permit_status(self, obj):
        return get_mark_safe(1) if obj.work_permit_date else get_mark_safe(0)

    def work_permit_dt(self, obj):
        return obj.work_permit_date.strftime('%d.%m.%y') if obj.work_permit_date else '-'

    def documents_send_status(self, obj):
        return get_mark_safe(1) if obj.documents_send_date else get_mark_safe(0)

    def documents_send_dt(self, obj):
        return obj.documents_send_date.strftime('%d.%m.%y') if obj.documents_send_date else '-'

    def work_invitation_dt(self, obj):
        return obj.work_invitation_date.strftime('%d.%m.%y') if obj.work_invitation_date else '-'

    def german_insurance_custom(self, obj):
        return get_mark_safe(1) if obj.german_insurance else get_mark_safe(0)

    def accomodation_status(self, obj):
        return get_mark_safe(1) if obj.accomodation else get_mark_safe(0)

    def accomodation_type(self, obj):
        return obj.get_accomodation_type_display() if obj.accomodation_type else '-'

    def german_work_contract_custom(self, obj):
        return get_mark_safe(1) if obj.german_work_contract else get_mark_safe(0)
    
    def nvks_custom(self, obj):
        return mark_safe(f'<strong style="color:red; font-size:1.5rem">НВКС</strong>') if obj.nvks else ''

    def payment(self, obj):
        return obj.paid_percent

    def export_xls(self, request):
        import xlwt

        queryset = self.get_queryset(request=request).order_by('termin', 'last_name', 'first_name')

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
        
        direction = request.GET.get('direction')

        if direction and direction in ['nord', 'sud']:
            queryset = queryset.filter(direction__exact=direction)

        year = request.GET.get('year__exact')

        if year and year.isdigit():
            queryset = queryset.filter(year=int(year))

        paper = request.GET.get('receipt_paper_confirm__exact')

        if paper and paper.isdigit():
            queryset = queryset.filter(receipt_paper_confirm__exact=util.strtobool(paper))

        employer_id = request.GET.get('employer__id__exact')

        if employer_id and employer_id.isdigit():
            queryset = queryset.filter(employer__id=int(employer_id))

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Профили")

        row_num = 0

        fields = [
            'full_name_reverse',
            'note',
            'comment',
            'bday',
            'termin_date',
            'termin_time',
            'zagranpassport_number_id',
            'zagranpassport_end_time',
            'university',
            'faculty',
            'year',
            'phone',
            'employer',
            'position',
            'work_period',
            'work_city',
            'receipt',
            'employer_confirm',
            'employer_confirm_dt',
            'zav_send_status',
            'zav_send_dt',
            'work_permit_status',
            'work_permit_dt',
            'documents_send_status',
            'documents_send_dt',
            'work_invitation_dt',
            'german_insurance_custom',
            'accomodation_status',
            'accomodation_type',
            'german_work_contract_custom',
            'payment',
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
    phone.short_description = 'Тел.'
    termin_date.short_description = 'Термин(д)'
    termin_time.short_description = 'Термин(вр)'
    employer.short_description = 'Работодатель'
    position.short_description = 'Должность'
    work_period.short_description = 'Период раб.'
    work_city.short_description = 'Город'
    receipt.short_description = 'Расписка'
    employer_confirm.short_description = 'Подтв. работод.'
    employer_confirm_dt.short_description = 'Подтв. работод.(дата)'
    zav_send_status.short_description = 'ZAV(статус)'
    zav_send_dt.short_description = 'ZAV(дата)'
    work_permit_status.short_description = 'Раб. разр(статус)'
    work_permit_dt.short_description = 'Раб. разр(дата)'
    documents_send_status.short_description = 'Экспресс отпр.'
    documents_send_dt.short_description = 'Экспресс дата'
    work_invitation_dt.short_description = 'Дата пол. пригл.'
    german_insurance_custom.short_description = 'Страховка'
    accomodation_status.short_description = 'Потв. жилья'
    accomodation_type.short_description = 'Жилье'
    german_work_contract_custom.short_description = 'Раб. дог.'
    payment.short_description = 'Оплата'
    zagranpassport_number_id.short_description = 'Номер заграна'
    zagranpassport_end_time_admin.short_description = 'Оконч. загр.'
    nvks_custom.short_description = 'НВКС'
