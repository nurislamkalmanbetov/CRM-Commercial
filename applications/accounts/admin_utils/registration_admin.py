import re

from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe

from applications.accounts.models import Profile
from .inlines import NotificationsInline, InterviewInline
from applications.accounts import filters
from applications.accounts.filters import CustomDateFilter
from applications.accounts.utils import get_mark_safe


class ProfileRegistrationAdmin(admin.ModelAdmin):
    inlines = [
        NotificationsInline,
        InterviewInline,
    ]

    class Media:
        css = {
            'all': ('admin/css/changelists_custom.css',)
        }
        js = ('admin/js/changelists_custom.js',)

    fields = [
        'user', 'photo', 'is_confirmed', 'is_form_completed', 'is_admin_confirmed',
        'access_to_registration_documents', 'access_to_embassy_documents', 'first_name', 'first_name_ru', 'last_name',
        'last_name_ru', 'gender', 'bday', 'characteristics', 'nvks',
        'nationality', 'passport_number', 'zagranpassport_number', 'zagranpassport_end_time',
        'embassy_visametric', 'termin', 'direction', 'university', 'faculty', 'degree', 'year',
        'study_start', 'study_end', 'summer_holidays_start', 'summer_holidays_end', 'start_vise_date',
        'end_vise_date', 'been_to_germany', 'level', 'courses_info', 'birth_country', 'birth_region',

        'study_certificate',  'study_certificate_confirm',
        'photo_for_schengen', 'photo_for_schengen_confirm',
        'zagranpassport_copy', 'zagranpassport_copy_confirm',
        'passport_copy', 'passport_copy_confirm',
        'fluorography_express', 'fluorography_express_confirm',
        'fluorography', 'fluorography_confirm',
        'immatrikulation', 'immatrikulation_download_date', 'immatrikulation_confirm', 'immatrikulation_paper_confirm',
        'contract_date',

        'birth_city', 'reg_region', 'reg_city', 'reg_city_en', 'reg_district', 'reg_district_en',
        'reg_street', 'reg_street_en', 'reg_house', 'reg_apartment', 'live_region', 'live_city',
        'live_city_en', 'live_district', 'live_district_en', 'live_street', 'live_street_en', 'live_house',
        'live_apartment', 'father_phone', 'father_work_phone', 'father_company', 'mother_phone', 'mother_work_phone',
        'mother_company', 'company1', 'position1', 'start_date1', 'end_date1', 'country1',
        'company2', 'position2', 'start_date2', 'end_date2', 'country2',
        'company3', 'position3', 'start_date3', 'end_date3', 'country3',
        'german', 'english', 'turkish', 'russian', 'chinese',
        'driver_license', 'driving_experience', 'cat_a', 'cat_b', 'cat_c', 'cat_d', 'cat_e', 'tractor',
        'transmission', 'bicycle_skill', 'shirt_size', 'pants_size', 'shoe_size',
        'reading', 'singing', 'travelling', 'yoga', 'dancing', 'sport', 'drawing', 'computer_games', 'guitar', 'films',
        'music', 'knitting', 'cooking', 'fishing', 'photographing', 'work_from', 'work_to',
        'agreement3', 'agreement3_download_date', 'act3', 'act3_download_date',
        'agreement1', 'agreement1_download_date', 'act1', 'act1_download_date',
        'agreement2', 'agreement2_download_date', 'act2', 'act2_download_date', 'consult_list', 'is_refused',
        'closure1', 'closure2', 'closure3',
    ]

    list_display = [
        'whatsapp_link',
        'full_name_reverse',
        'nvks_custom',
        'note_form',
        'comment_form',
        'university_admin',
        'faculty_admin',
        'year',
        'termin_date',
        'termin_time',
        'phone',
        'level',
        'courses_info',
        'bday',
        'zagranpassport_number_id',
        'zagranpassport_end_time_admin',
        'zagranpassport_copy_status',
        'passport_number_id',
        'passport_copy_status',
        'gender',
        'summer_holidays_start',
        'summer_holidays_end',
        'jipl_paper_confirm_admin',
        'resume_admin',
        'immat_admin',
        'work_contract_admin',
        'traning_contract_admin',
        'photo_admin',
        'receipt_paper_admin',
        'study_certificate_admin',
        'fluorography_admin',
        'contract_dt',
        'payment',
        'agreement3',
        'act3',
        'agreement1', 
        'act1', 
        'agreement2', 
        'act2',
        'consult_list'
    ]

    readonly_fields = ('agreement1_download_date', 
                       'agreement2_download_date', 
                       'agreement3_download_date', 
                       'act1_download_date', 
                       'act2_download_date', 
                       'act3_download_date',
                       'immatrikulation_download_date',
                       )

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
        'level',
        filters.DirectionFilter,
        filters.NvksFilter,
        filters.ZagranPassportCopy,
        filters.PassportCopy,
        filters.JIPLConfirm,
        filters.ResumeConfirm,
        filters.IMMATConfirm,
        filters.WorkContractConfirm,
        filters.TrainingContractConfirm,
        filters.PhotoConfirm,
        filters.ReceiptConfirm,
        filters.FluorographyConfirm,
        filters.StudyCertificateConfirm,
        filters.GermanyExperience,
        ('summer_holidays_start', CustomDateFilter),
        ('summer_holidays_end', CustomDateFilter),
        ('study_start', filters.CustomDateFilter),
        ('study_end', filters.CustomDateFilter)
    ]

    change_list_template = 'admin/accounts/change_list.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        profile = get_object_or_404(Profile, pk=object_id)
        if profile and profile.photo:
            extra_context['photo_url'] = profile.photo.url
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):

        if request.GET.get('get_xls', None):
            return self.export_xls(request)

        extra_context = extra_context or {}
        extra_context['table_classname'] = 'confirmed'
        return super(ProfileRegistrationAdmin, self).changelist_view(request, extra_context=extra_context)

    def whatsapp_link(self, obj):
        return mark_safe(f'<a href="https://api.whatsapp.com/send?phone={obj.user.whatsapp_phone}" target="_blank" title="Написать на {obj.user.whatsapp_phone}"><img src="/static/images/icons/whatsapp.svg" width="18" height="18" /></a>')

    def full_name_reverse(self, obj):
        return mark_safe(f'<a href="/admin/accounts/profileinregistration/{obj.id}/change" title="{obj.full_name_reverse}">{obj.full_name_reverse}</a>')

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
                                
    def university_admin(self, obj):
        return obj.university

    def faculty_admin(self, obj):
        return obj.faculty

    def phone(self, obj, xls=False):
        return obj.user.phone

    def passport_number_id(self, obj, xls=False):
        return obj.passport_number

    def passport_copy_status(self, obj, xls=False):
        if xls:
            if obj.passport_copy_confirm and obj.passport_copy_paper_confirm:
                return "Обе копии"
            elif obj.passport_copy_confirm or obj.passport_copy_paper_confirm:
                return "Одна копия"
            return "Нет копий"
        if obj.passport_copy_confirm and obj.passport_copy_paper_confirm:
            return get_mark_safe(2)
        elif obj.passport_copy_confirm or obj.passport_copy_paper_confirm:
            return get_mark_safe(1)
        return get_mark_safe(0)

    def zagranpassport_number_id(self, obj, xls=False):
        return obj.zagranpassport_number

    def zagranpassport_copy_status(self, obj, xls=False):
        if xls:
            if obj.zagranpassport_copy_confirm and obj.zagranpassport_copy_paper_confirm:
                return "Обе копии"
            elif obj.zagranpassport_copy_confirm or obj.zagranpassport_copy_paper_confirm:
                return "Одна копия"
            return "Нет копий"
        if obj.zagranpassport_copy_confirm and obj.zagranpassport_copy_paper_confirm:
            return get_mark_safe(2)
        elif obj.zagranpassport_copy_confirm or obj.zagranpassport_copy_paper_confirm:
            return get_mark_safe(1)
        return get_mark_safe(0)

    def zagranpassport_end_time_admin(self, obj, xls=False):
        return obj.zagranpassport_end_time

    def termin_date(self, obj, xls=False):
        return obj.termin.strftime('%d.%m.%y') if obj.termin else '-'

    def termin_time(self, obj, xls=False):
        return obj.termin.strftime('%H:%M') if obj.termin else '-'

    def jipl_paper_confirm_admin(self, obj, xls=False):
        if xls:
            return 'Есть копия' if obj.jipl_paper_confirm else 'Нет копии'
        return get_mark_safe(1) if obj.jipl_paper_confirm else get_mark_safe(0)

    def resume_admin(self, obj, xls=False):
        if xls:
            return 'Есть копия' if obj.jipl_paper_confirm else 'Нет копии'
        return get_mark_safe(1) if obj.resume_paper_confirm else get_mark_safe(0)

    def immat_admin(self, obj, xls=False):
        if xls:
            if obj.immatrikulation_confirm and obj.immatrikulation_paper_confirm:
                return "Обе копии"
            elif obj.immatrikulation_confirm or obj.immatrikulation_paper_confirm:
                return "Одна копия"
            elif obj.immatrikulation:
                return "Не подтверждено"
            return "Нет копий"
        if obj.immatrikulation_confirm and obj.immatrikulation_paper_confirm:
            return get_mark_safe(2)
        elif obj.immatrikulation_confirm or obj.immatrikulation_paper_confirm:
            return get_mark_safe(1)
        elif obj.immatrikulation:
            return get_mark_safe(-1)
        return get_mark_safe(0)

    def work_contract_admin(self, obj, xls=False):
        if xls:
            return 'Есть копия' if obj.work_contract_paper_confirm else 'Нет копии'
        return get_mark_safe(1) if obj.work_contract_paper_confirm else get_mark_safe(0)

    def traning_contract_admin(self, obj, xls=False):
        if xls:
            return 'Есть копия' if obj.traning_contract_paper_confirm else 'Нет копии'
        return get_mark_safe(1) if obj.traning_contract_paper_confirm else get_mark_safe(0)

    def photo_admin(self, obj, xls=False):
        if xls:
            if obj.photo_for_schengen_confirm and obj.photo_for_schengen_paper_confirm:
                return "Есть фото"
            elif obj.photo_for_schengen_confirm or obj.photo_for_schengen_paper_confirm:
                return "Одно фото"
            return "Нет фото"
        if obj.photo_for_schengen_confirm and obj.photo_for_schengen_paper_confirm:
            return get_mark_safe(2)
        elif obj.photo_for_schengen_confirm or obj.photo_for_schengen_paper_confirm:
            return get_mark_safe(1)
        return get_mark_safe(0)

    def receipt_paper_admin(self, obj, xls=False):
        if xls:
            return 'Есть копия' if obj.receipt_paper_confirm else 'Нет копии'
        return get_mark_safe(1) if obj.receipt_paper_confirm else get_mark_safe(0)

    def study_certificate_admin(self, obj, xls=False):
        if xls:
            if obj.study_certificate_paper_confirm and obj.study_certificate_confirm:
                return "Обе копии"
            elif obj.study_certificate_paper_confirm or obj.study_certificate_confirm:
                return "Одна копия"
            return "Нет копий"
        if obj.study_certificate_paper_confirm and obj.study_certificate_confirm:
            return get_mark_safe(2)
        elif obj.study_certificate_paper_confirm or obj.study_certificate_confirm:
            return get_mark_safe(1)
        return get_mark_safe(0)

    def fluorography_admin(self, obj, xls=False):
        if xls:
            if obj.fluorography_paper_confirm and obj.fluorography_confirm:
                return "Обе копии"
            elif obj.fluorography_paper_confirm or obj.fluorography_confirm:
                return "Одна копия"
            return "Нет копий"
        if obj.fluorography_paper_confirm and obj.fluorography_confirm:
            return get_mark_safe(2)
        elif obj.fluorography_paper_confirm or obj.fluorography_confirm:
            return get_mark_safe(1)
        return get_mark_safe(0)

    def contract_dt(self, obj, xls=False):
        return obj.contract_date.strftime('%d.%m.%y') if obj.contract_date else '-'

    def payment(self, obj, xls=False):
        return obj.paid_percent
    
    def nvks_custom(self, obj):
        return mark_safe(f'<strong style="color:red; font-size:1.5rem">НВКС</strong>') if obj.nvks else ''

    def export_xls(self, request):
        import xlwt

        queryset = self.get_queryset(request=request).order_by('last_name', 'first_name')

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

        lvl = request.GET.get('level__exact')

        if lvl:
            queryset = queryset.filter(level=lvl)

        year = request.GET.get('year__exact')

        if year and year.isdigit():
            queryset = queryset.filter(year=int(year))

        direction = request.GET.get('direction')

        if direction and direction in ['nord', 'sud']:
            queryset = queryset.filter(direction__exact=direction)

        int_pass_id = request.GET.get('int_pass_id')

        if int_pass_id and int_pass_id in ['copy_confirm',
                                           'paper_copy_confirm',
                                           'twice_confirm',
                                           'not_confirm']:

            if int_pass_id == 'copy_confirm':
                queryset.filter(zagranpassport_copy_confirm=True)
            if int_pass_id == 'paper_copy_confirm':
                queryset.filter(zagranpassport_copy_paper_confirm=True)
            if int_pass_id == 'twice_confirm':
                queryset.filter(zagranpassport_copy_confirm=True, zagranpassport_copy_paper_confirm=True)
            if int_pass_id == 'not_confirm':
                queryset.filter(zagranpassport_copy_confirm=False, zagranpassport_copy_paper_confirm=False)

        passport_copy = request.GET.get('passport_copy')

        if passport_copy and passport_copy in ['copy_confirm',
                                           'paper_copy_confirm',
                                           'twice_confirm',
                                           'not_confirm']:
            if passport_copy == 'copy_confirm':
                queryset.filter(passport_copy_confirm=True)
            if passport_copy == 'paper_copy_confirm':
                queryset.filter(passport_copy_paper_confirm=True)
            if passport_copy == 'twice_confirm':
                queryset.filter(passport_copy_confirm=True, passport_copy_paper_confirm=True)
            if passport_copy == 'not_confirm':
                queryset.filter(passport_copy_confirm=False, passport_copy_paper_confirm=False)

        jipl = request.GET.get('JIPL')

        if jipl and jipl in ['paper_copy_confirm','not_paper_copy_confirm']:
            if jipl == 'paper_copy_confirm':
                queryset.filter(jipl_paper_confirm=True)
            if jipl == 'not_paper_copy_confirm':
                queryset.filter(jipl_paper_confirm=False)

        resume = request.GET.get('resume')

        if resume and resume in ['confirmed','not_confirmed']:
            if resume == 'confirmed':
                queryset.filter(resume_paper_confirm=True)
            if resume == 'not_confirmed':
                queryset.filter(resume_paper_confirm=False)

        immat = request.GET.get('IMMAT')

        if immat and immat in ['immatrikulation',
                               'immatrikulation_confirm',
                               'immatrikulation_paper_confirm',
                               'twice_confirm',
                               'not_confirm']:
            if immat == 'immatrikulation':
                queryset.exclude(immatrikulation__isnull=False)
            if immat == 'immatrikulation_confirm':
                queryset.filter(immatrikulation_confirm=True)
            if immat == 'immatrikulation_paper_confirm':
                queryset.filter(immatrikulation_paper_confirm=True)
            if immat == 'twice_confirm':
                queryset.filter(immatrikulation_confirm=True, immatrikulation_paper_confirm=True)
            if immat == 'not_confirm':
                queryset.filter(immatrikulation_confirm=False, immatrikulation_paper_confirm=False)

        labor = request.GET.get('labor_agreement')

        if labor and labor in ['paper_copy_confirm','not_paper_copy_confirm']:
            if labor == 'paper_copy_confirm':
                queryset.filter(work_contract_paper_confirm=True)
            if labor == 'not_paper_copy_confirm':
                queryset.filter(work_contract_paper_confirm=False)

        train = request.GET.get('training_agreement')

        if train and train in ['paper_copy_confirm','not_paper_copy_confirm']:
            if train == 'paper_copy_confirm':
                queryset.filter(traning_contract_paper_confirm=True)
            if train == 'not_paper_copy_confirm':
                queryset.filter(traning_contract_paper_confirm=False)

        shen = request.GET.get('shengen_photo')

        if shen and shen in ['copy_confirm',
                             'paper_copy_confirm',
                             'twice_confirm',
                             'not_confirm']:
            if shen == 'paper_copy_confirm':
                queryset.filter(photo_for_schengen_paper_confirm=True)
            if shen == 'copy_confirm':
                queryset.filter(photo_for_schengen_confirm=True)
            if shen == 'twice_confirm':
                queryset.filter(photo_for_schengen_paper_confirm=True, photo_for_schengen_confirm=True)
            if shen == 'not_confirm':
                queryset.filter(photo_for_schengen_paper_confirm=False, photo_for_schengen_confirm=False)

        raspiska = request.GET.get('raspiska')

        if raspiska and raspiska in ['paper_copy_confirm','not_paper_copy_confirm']:
            if raspiska == 'paper_copy_confirm':
                queryset.filter(receipt_paper_confirm=True)
            if raspiska == 'not_paper_copy_confirm':
                queryset.filter(receipt_paper_confirm=False)

        fluro = request.GET.get('chest_xray')

        if fluro and fluro in ['copy_confirm',
                               'paper_copy_confirm',
                               'twice_confirm',
                               'not_confirm']:
            if fluro == 'paper_copy_confirm':
                queryset.filter(fluorography_paper_confirm=True)
            if fluro == 'copy_confirm':
                queryset.filter(fluorography_confirm=True)
            if fluro == 'twice_confirm':
                queryset.filter(fluorography_paper_confirm=True, fluorography_confirm=True)
            if fluro == 'not_confirm':
                queryset.filter(fluorography_paper_confirm=False, fluorography_confirm=False)

        spr = request.GET.get('student_note')

        if spr and spr in ['copy_confirm',
                            'paper_copy_confirm',
                            'twice_confirm',
                            'not_confirm']:
            if spr == 'paper_copy_confirm':
                queryset.filter(study_certificate_paper_confirm=True)
            if spr == 'copy_confirm':
                queryset.filter(study_certificate_confirm=True)
            if spr == 'twice_confirm':
                queryset.filter(study_certificate_paper_confirm=True, study_certificate_confirm=True)
            if spr == 'not_confirm':
                queryset.filter(study_certificate_paper_confirm=False, study_certificate_confirm=False)

        exp = request.GET.get('been_to_germany')

        if exp and exp in ['yes', 'no']:
            if exp == 'yes':
                queryset.filter(
                    Q(country1='Deutschland') | Q(country2='Deutschland') | Q(country3='Deutschland'))
            if exp == 'no':
                queryset.exclude(
                    Q(country1='Deutschland') | Q(country2='Deutschland') | Q(country3='Deutschland'))

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
            'Имя на кириллице',
            'Заметка',
            'Комментарий',
            'Университет',
            'Факультет',
            'Курс',
            'Дата термин посольство',
            'Время термин посольство',
            'Номер',
            'Уровень',
            'Курсы',
            'День рождения',
            'Номер загранпаспорта',
            'Дата окончания загранпаспорта',
            'Копия загранпаспорта',
            'Номер ID',
            'Копия ID',
            'Пол',
            'Дата начала каникул',
            'Дата окончания каникул',
            'ЖИПЛ',
            'Резюме',
            'Immat',
            'Дог.труд.',
            'Дог.Трен.',
            'Фото',
            'Расписка',
            'Спр.с.ун.',
            'Флюра',
            'Дата договора',
            'Оплата',
        ]

        fields = [
            'full_name_reverse',
            'full_name_ru',
            'note',
            'comment',
            'university',
            'faculty',
            'year',
            'termin_date',
            'termin_time',
            'phone',
            'level',
            'courses_info',
            'bday',
            'zagranpassport_number_id',
            'zagranpassport_end_time',
            'zagranpassport_copy_status',
            'passport_number_id',
            'passport_copy_status',
            'gender',
            'summer_holidays_start',
            'summer_holidays_end',
            'jipl_paper_confirm_admin',
            'resume_admin',
            'immat_admin',
            'work_contract_admin',
            'traning_contract_admin',
            'photo_admin',
            'receipt_paper_admin',
            'study_certificate_admin',
            'fluorography_admin',
            'contract_dt',
            'payment',
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

                    if type(value) != int or type(value) != float or not value:
                        value = str(value)
                    row.append(value)
                else:
                    row.append(getattr(self, field)(obj, True))
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

    export_xls.short_description = u"Export XLS"

    payment.short_description = 'Оплачено'
    whatsapp_link.short_description = mark_safe(f'<img src="/static/images/icons/whatsapp.svg" width="18" height="18" />')
    full_name_reverse.short_description = 'Имя'
    note_form.short_description = 'Заметка'
    comment_form.short_description = 'Коммент.'
    university_admin.short_description = 'Унив.'
    faculty_admin.short_description = 'Фак.'
    phone.short_description = 'Тел.'
    passport_number_id.short_description = 'ID'
    passport_copy_status.short_description = 'Коп. ID'
    zagranpassport_number_id.short_description = 'Номер заграна'
    zagranpassport_copy_status.short_description = 'Коп. загр.'
    termin_date.short_description = 'Термин(д)'
    termin_time.short_description = 'Термин(вр)'
    zagranpassport_end_time_admin.short_description = 'Оконч. загр.'
    jipl_paper_confirm_admin.short_description = 'ЖИПЛ'
    resume_admin.short_description = 'Резюме'
    immat_admin.short_description = 'Immat'
    work_contract_admin.short_description = 'Труд.'
    traning_contract_admin.short_description = 'Трен.'
    photo_admin.short_description = 'Фото'
    receipt_paper_admin.short_description = 'Расп'
    study_certificate_admin.short_description = 'Спр.с.ун.'
    fluorography_admin.short_description = 'Флюра'
    contract_dt.short_description = 'Дог д.'
    nvks_custom.short_description = 'НВКС'
