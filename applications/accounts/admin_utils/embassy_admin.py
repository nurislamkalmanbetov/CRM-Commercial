import re
from distutils import util

from django.db.models import Q
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils.safestring import mark_safe, SafeText

from .inlines import NotificationsInline, InterviewInline
from applications.accounts.models import Profile, ProfileInEmbassy
from applications.accounts import filters
from applications.accounts.filters import CustomDateFilter
from applications.accounts.utils import get_mark_safe


class ProfileInEmbassyAdmin(admin.ModelAdmin):
    inlines = [
        NotificationsInline,
        InterviewInline,
    ]

    fields = [
        'first_name', 'last_name', 'bday', 'passport_number', 'zagranpassport_number', 'zagranpassport_end_time',
        'in_review', 'embassy_visametric', 'termin', 'start_vise_date', 'end_vise_date', 'visa_file', 
        'university', 'faculty', 'year', 'zagranpassport_copy', 'invitation',
        'labor_agreement', 'liveplace_approve', 'insurance',
        'fluorography', 'fluorography_confirm',
        'transcript', 'transcript_confirm', 'transcript_paper_confirm',
        'bank_statement', 'bank_statement_confirm', 'bank_statement_paper_confirm',
        'conduct_certificate', 'conduct_certificate_confirm', 'conduct_certificate_paper_confirm',
        'mentaldispanser_certificate', 'mentaldispanser_certificate_confirm', 'mentaldispanser_certificate_paper_confirm',
        'drugdispanser_certificate', 'drugdispanser_certificate_confirm', 'drugdispanser_certificate_paper_confirm',
        'parental_permission', 'parental_permission_confirm', 'parental_permission_paper_confirm',
        'bank_details', 'bank_details_confirm', 'bank_details_paper_confirm',
        'work_permit_date', 'work_invitation_date', 'documents_send_date',
        'local_insurance', 'german_insurance', 'accomodation', 'accomodation_type', 'german_work_contract', 'embassy_anketa',
        'transcript_translate', 'transcript_translate_confirm', 'transcript_translate_paper_confirm',
        'study_certificate_embassy', 'study_certificate_embassy_confirm', 'study_certificate_paper_embassy_confirm',
        'study_certificate_translate_embassy', 'study_certificate_translate_embassy_confirm', 'study_certificate_translate_paper_embassy_confirm',
        'documents_collected_by', 'consultant', 'full_sum', 'consult_date', 'visa_reject',
        'loan', 
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
        'embassy_visametric_custom',
        'employer',
        'work_period',
        'visa_period',
        'invited',
        'insurance',
        'accomodation_status_custom',
        'german_work_contract_custom',
        'university_document_embassy',
        'university_document_translate_embassy',
        'transcript_original',
        'transcript_translation',
        'bank_document',
        'photography',
        'anketa_embassy',
        'zagran',
        'nesudimost',
        'narko',
        'psycho',
        'parent_permissions',
        'bank_details',
        'fluorography_embassy',
        'documents_collected_by',
        'consultant',
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
        filters.GermanyInvitation,
        filters.GermanyInsurance,
        filters.LocalInsurance,
        filters.Accomodation,
        filters.WorkContract,
        filters.UniversityDocumentEmbassy,
        filters.UniversityDocumentTranslationEmbassy,
        filters.UniversityTranscript,
        filters.UniversityTranscriptTranslation,
        filters.BankStatement,
        filters.PhotoFile,
        filters.PhotoPaper,
        filters.EmbassyAnketa,
        filters.ZagranPassport,
        filters.MVD,
        filters.Narkodispanser,
        filters.Psihdispanser,
        filters.ParentsPermission,
        filters.BankAccountDetails,
        ('termin', CustomDateFilter),
        ('study_start', CustomDateFilter),
        ('study_end', CustomDateFilter),
        filters.InReview,
        filters.VisaFileFilter,
        'visa_reject',
    ]

    change_list_template = 'admin/accounts/change_list.html'

    ordering = ['-in_review', '-termin']

    class Media:
        css = {
            'all': ('admin/css/changelists_custom.css',)
        }
        js = ('admin/js/changelists_custom.js',)

    def changelist_view(self, request, extra_context=None):

        if request.GET.get('get_xls', None):
            return self.export_xls(request)

        extra_context = extra_context or {}
        extra_context['table_classname'] = 'embassy'
        return super(ProfileInEmbassyAdmin, self).changelist_view(request, extra_context=extra_context)

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
            f'<a href="/admin/accounts/profileinembassy/{obj.id}/change?next=/admin/accounts/profileinembassy/" title="{obj.full_name_reverse}">{obj.full_name_reverse}</a>')

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

    def employer(self, obj, xls=False):
        return obj.company_name if obj.company_name else '-'

    def work_period(self, obj, xls=False):
        return f'{obj.work_from.strftime("%d.%m.%y")}-{obj.work_to.strftime("%d.%m.%y")}' if obj.work_from and obj.work_to else '-'

    def visa_period(self, obj, xls=False):
        return f'{obj.start_vise_date.strftime("%d.%m.%y")}-{obj.end_vise_date.strftime("%d.%m.%y")}'\
            if obj.start_vise_date and obj.end_vise_date else '-'

    def german_work_contract_custom(self, obj, xls=False):
        return get_mark_safe(1) if obj.german_work_contract else get_mark_safe(0)

    def accomodation_status_custom(self, obj, xls=False):
        return get_mark_safe(1) if obj.accomodation_type == 'employer' else get_mark_safe(0)

    def embassy_visametric_custom(self, obj, xls=False):
        return obj.get_embassy_visametric_display() if obj.embassy_visametric else '-'

    def invited(self, obj, xls=False):
        return get_mark_safe(1) if obj.work_invitation_date else get_mark_safe(0)

    def insurance(self, obj, xls=False):
        return get_mark_safe(1) if obj.german_insurance or obj.local_insurance else get_mark_safe(0)

    def university_document_embassy(self, obj, xls=False):
        if (obj.study_certificate_embassy and obj.study_certificate_embassy_confirm) or obj.study_certificate_paper_embassy_confirm:
            return get_mark_safe(1)
        elif obj.study_certificate_embassy and obj.study_certificate_embassy_confirm and obj.study_certificate_paper_embassy_confirm:
            return get_mark_safe(2)
        elif obj.study_certificate_embassy and not obj.study_certificate_embassy_confirm:
            return get_mark_safe(3)
        return get_mark_safe(0)

    def university_document_translate_embassy(self, obj, xls=False):
        if (obj.study_certificate_translate_embassy and obj.study_certificate_translate_embassy_confirm) or obj.study_certificate_translate_paper_embassy_confirm:
            return get_mark_safe(1)
        elif obj.study_certificate_translate_embassy and obj.study_certificate_translate_embassy_confirm and obj.study_certificate_translate_paper_embassy_confirm:
            return get_mark_safe(2)
        elif obj.study_certificate_translate_embassy and not obj.study_certificate_translate_embassy_confirm:
            return get_mark_safe(3)
        return get_mark_safe(0)

    def transcript_original(self, obj, xls=False):
        if (obj.transcript and obj.transcript_confirm) or obj.transcript_paper_confirm:
            return get_mark_safe(1)
        elif obj.transcript and obj.transcript_confirm and obj.transcript_paper_confirm:
            return get_mark_safe(2)
        elif obj.transcript and not obj.transcript_confirm:
            return get_mark_safe(3)
        return get_mark_safe(0)

    def transcript_translation(self, obj, xls=False):
        if (obj.transcript_translate and obj.transcript_translate_confirm) or obj.transcript_translate_paper_confirm:
            return get_mark_safe(1)
        elif obj.transcript_translate and obj.transcript_translate_confirm and obj.transcript_translate_paper_confirm:
            return get_mark_safe(2)
        elif obj.transcript_translate and not obj.transcript_translate_confirm:
            return get_mark_safe(3)
        return get_mark_safe(0)

    def bank_document(self, obj, xls=False):
        if (obj.bank_statement and obj.bank_statement_confirm) or obj.bank_statement_paper_confirm:
            return get_mark_safe(1)
        elif obj.bank_statement and obj.bank_statement_confirm and obj.bank_statement_paper_confirm:
            return get_mark_safe(2)
        elif obj.bank_statement and not obj.bank_statement_confirm:
            return get_mark_safe(3)
        return get_mark_safe(0)

    def photography(self, obj, xls=False):
        if (obj.photo_for_schengen and obj.photo_for_schengen_confirm) or obj.photo_for_schengen_paper_confirm:
            return get_mark_safe(1)
        elif obj.photo_for_schengen and obj.photo_for_schengen_confirm and obj.photo_for_schengen_paper_confirm:
            return get_mark_safe(2)
        elif obj.photo_for_schengen and not obj.photo_for_schengen_confirm:
            return get_mark_safe(3)
        return get_mark_safe(0)

    def anketa_embassy(self, obj, xls=False):
        return get_mark_safe(1) if obj.embassy_anketa else get_mark_safe(0)

    def zagran(self, obj, xls=False):
        if (obj.zagranpassport_copy and obj.zagranpassport_copy_confirm) or obj.zagranpassport_copy_paper_confirm:
            return get_mark_safe(1)
        elif obj.zagranpassport_copy and obj.zagranpassport_copy_confirm and obj.zagranpassport_copy_paper_confirm:
            return get_mark_safe(2)
        elif obj.zagranpassport_copy and not obj.zagranpassport_copy_confirm:
            return get_mark_safe(3)
        return get_mark_safe(0)

    def nesudimost(self, obj, xls=False):
        if (obj.conduct_certificate and obj.conduct_certificate_confirm) or obj.conduct_certificate_paper_confirm:
            return get_mark_safe(1)
        elif obj.conduct_certificate and obj.conduct_certificate_confirm and obj.conduct_certificate_paper_confirm:
            return get_mark_safe(2)
        elif obj.conduct_certificate and not obj.conduct_certificate_confirm:
            return get_mark_safe(3)
        return get_mark_safe(0)

    def narko(self, obj, xls=False):
        if (obj.drugdispanser_certificate and obj.drugdispanser_certificate_confirm) or obj.drugdispanser_certificate_paper_confirm:
            return get_mark_safe(1)
        elif obj.drugdispanser_certificate and obj.drugdispanser_certificate_confirm and obj.drugdispanser_certificate_paper_confirm:
            return get_mark_safe(2)
        elif obj.drugdispanser_certificate and not obj.drugdispanser_certificate_confirm:
            return get_mark_safe(3)
        return get_mark_safe(0)

    def psycho(self, obj, xls=False):
        if (obj.mentaldispanser_certificate and obj.mentaldispanser_certificate_confirm) or obj.mentaldispanser_certificate_paper_confirm:
            return get_mark_safe(1)
        elif obj.mentaldispanser_certificate and obj.mentaldispanser_certificate_confirm and obj.mentaldispanser_certificate_paper_confirm:
            return get_mark_safe(2)
        elif obj.mentaldispanser_certificate and not obj.mentaldispanser_certificate_confirm:
            return get_mark_safe(3)
        return get_mark_safe(0)

    def parent_permissions(self, obj, xls=False):
        if (obj.parental_permission and obj.parental_permission_confirm) or obj.parental_permission_paper_confirm:
            return get_mark_safe(1)
        elif obj.parental_permission and obj.parental_permission_confirm and obj.parental_permission_paper_confirm:
            return get_mark_safe(2)
        elif obj.parental_permission and not obj.parental_permission_confirm:
            return get_mark_safe(3)
        return get_mark_safe(0)

    def bank_details(self, obj, xls=False):
        if (obj.bank_details and obj.bank_details_confirm) or obj.bank_details_paper_confirm:
            return get_mark_safe(1)
        elif obj.bank_details and obj.bank_details_confirm and obj.bank_details_paper_confirm:
            return get_mark_safe(2)
        elif obj.bank_details and not obj.bank_details_confirm:
            return get_mark_safe(3)
        return get_mark_safe(0)

    def fluorography_embassy(self, obj, xls=False):
        if (obj.fluorography and obj.fluorography_confirm) or obj.fluorography_paper_confirm:
            return get_mark_safe(1)
        elif obj.fluorography and obj.fluorography_confirm and obj.fluorography_paper_confirm:
            return get_mark_safe(2)
        elif obj.fluorography and not obj.fluorography_confirm:
            return get_mark_safe(3)
        return get_mark_safe(0)

    def nvks_custom(self, obj):
        return mark_safe(f'<strong style="color:red; font-size:1.5rem">НВКС</strong>') if obj.nvks else ''

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

        year = request.GET.get('year__exact')

        if year and year.isdigit():
            queryset = queryset.filter(year=int(year))

        invitation = request.GET.get('invitation')

        direction = request.GET.get('direction')

        if direction and direction in ['nord', 'sud']:
            queryset = queryset.filter(direction__exact=direction)

        if invitation and invitation in ['yes', 'no']:
            if invitation == 'yes':
                queryset.exclude(work_invitation_date__isnull=True)
            if invitation == 'no':
                queryset.filter(work_invitation_date__isnull=True)

        german_insurance= request.GET.get('german_insurance')

        if german_insurance and german_insurance in ['yes', 'no']:
            queryset = queryset.filter(german_insurance = util.strtobool(german_insurance))

        local_insurance = request.GET.get('local_insurance')

        if local_insurance and local_insurance in ['yes', 'no']:
            queryset = queryset.filter(local_insurance=util.strtobool(local_insurance))

        accomodation = request.GET.get('accomodation')

        if accomodation and accomodation in ['yes', 'no']:
            queryset = queryset.filter(accomodation=util.strtobool(accomodation))

        german_work_contract = request.GET.get('german_work_contract')

        if german_work_contract and german_work_contract in ['yes', 'no']:
            queryset = queryset.filter(german_work_contract=util.strtobool(german_work_contract))

        asd = request.GET.get('study_certificate_paper_embassy_confirm')

        if asd and asd in['yes', 'no']:
            queryset = queryset.filter(study_certificate_paper_embassy_confirm=util.strtobool(asd))

        study_paper = request.GET.get('study_certificate_translate_paper_embassy_confirm')

        if study_paper and study_paper in ['yes', 'no']:
            queryset = queryset.filter(study_certificate_translate_paper_embassy_confirm=util.strtobool(study_paper))

        transcript_paper_confirm = request.GET.get('transcript_paper_confirm')

        if transcript_paper_confirm and transcript_paper_confirm in ['yes', 'no']:
            queryset = queryset.filter(transcript_paper_confirm=util.strtobool(transcript_paper_confirm))

        tcp = request.GET.get('transcript_translate_paper_confirm')

        if tcp and tcp in ['yes', 'no']:
            queryset = queryset.filter(transcript_translate_paper_confirm=util.strtobool(tcp))

        bank = request.GET.get('bank_statement_paper_confirm')

        if bank and bank in ['yes', 'no']:
            queryset = queryset.filter(bank_statement_paper_confirm=util.strtobool(bank))

        photo = request.GET.get('photo_for_schengen')

        if photo and photo in ['yes', 'no']:
            if photo == 'yes':
                queryset.exclude(Q(photo_for_schengen__isnull=True) | Q(photo_for_schengen=''))
            if photo == 'no':
                queryset.filter(Q(photo_for_schengen__isnull=True) | Q(photo_for_schengen=''))

        paper_photo = request.GET.get('photo_for_schengen_paper_confirm')

        if paper_photo and paper_photo in ['yes', 'no']:
            queryset = queryset.filter(photo_for_schengen_paper_confirm = util.strtobool(paper_photo))

        embassy_anketa = request.GET.get('embassy_anketa')

        if embassy_anketa and embassy_anketa in ['yes', 'no']:
            queryset = queryset.filter(embassy_anketa=util.strtobool(embassy_anketa))

        zagr = request.GET.get('zagranpassport_copy_paper_confirm')

        if zagr and zagr in ['yes', 'no']:
            queryset = queryset.filter(zagranpassport_copy_paper_confirm=util.strtobool(zagr))

        mvd = request.GET.get('conduct_certificate_paper_confirm')

        if mvd and mvd in ['yes', 'no']:
            queryset = queryset.filter(conduct_certificate_paper_confirm=util.strtobool(mvd))

        nark = request.GET.get('drugdispanser_certificate_paper_confirm')

        if nark and nark in ['yes', 'no']:
            queryset = queryset.filter(drugdispanser_certificate_paper_confirm=util.strtobool(nark))

        mental = request.GET.get('mentaldispanser_certificate_paper_confirm')

        if mental and mental in ['yes', 'no']:
            queryset = queryset.filter(mentaldispanser_certificate_paper_confirm=util.strtobool(mental))

        parents = request.GET.get('parental_permission_paper_confirm')

        if parents and parents in ['yes', 'no']:
            queryset = queryset.filter(parental_permission_paper_confirm=util.strtobool(parents))

        banko = request.GET.get('bank_details_paper_confirm')

        if banko and banko in ['yes', 'no']:
            queryset = queryset.filter(bank_details_paper_confirm=util.strtobool(banko))

        termin_strt = request.GET.get('termin__range__gte')
        termin_fnsh = request.GET.get('termin__range__lte')

        if termin_strt and re.match('\d{2}.\d{2}.\d{4}', termin_strt):
            termin_strt = ('-').join(termin_strt.split('.')[::-1])
            queryset = queryset.filter(termin__gte=termin_strt)

        if termin_fnsh and re.match('\d{2}.\d{2}.\d{4}', termin_fnsh):
            termin_fnsh = ('-').join(termin_fnsh.split('.')[::-1])
            queryset = queryset.filter(termin__lte=termin_fnsh)


        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Профили")

        row_num = 0

        columns = [
            'Имя',
            'Заметка',
            'Комментарий',
            'Дата термина посольство',
            'Время термина посольство',
            'День рождения',
            'Номер загранпаспорта',
            'Дата окончания загранпаспорта',
            'Университет',
            'Факультет',
            'Курс',
            'Номер',
            'Уровень',
            'Курсы',

            'Посольство/Визаметрик',
            'Работодатель',
            'Даты работы',
            'Даты визы',
            'Приглашен',
            'Страховка',
            'Подтверждение жилья',
            'Рабочий договор',
            'Справка с университета',
            'Перевод справки с университета',
            'Транскрипт',
            'Перевод транскрипта',
            'Выписка с банка',
            'Фото',
            'Анкета для посольства',
            'Загранпаспорт',
            'МВД',
            'Наркодиспансер',
            'Психодиспансер',
            'Разрешение от родителей',
            'Реквизиты банка'
            'Флюрография',
            'Сбор документов осуществлен админом',
            'Консультант',
        ]

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
            'termin_date',
            'termin_time',
            'embassy_visametric_custom',
            'employer',
            'work_period',
            'visa_period',
            'invited',
            'insurance',
            'accomodation_status_custom',
            'german_work_contract_custom',
            'university_document_embassy',
            'university_document_translate_embassy',
            'transcript_original',
            'transcript_translation',
            'bank_document',
            'photography',
            'anketa_embassy',
            'zagran',
            'nesudimost',
            'narko',
            'psycho',
            'parent_permissions',
            'bank_details',
            'fluorography_embassy',
            'documents_collected_by',
            'consultant',
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
    embassy_visametric_custom.short_description = 'Пос./Визам.'
    employer.short_description = 'Работодатель'
    work_period.short_description = 'Даты работы'
    visa_period.short_description = 'Даты визы'
    german_work_contract_custom.short_description = 'Рабочий дог.'
    invited.short_description = 'Приглаш.'
    insurance.short_description = 'Страх.'
    accomodation_status_custom.short_description = 'Подтв. жилья'
    university_document_embassy.short_description = 'Спр. с ун.'
    university_document_translate_embassy.short_description = 'Спр. с ун.(пер)'
    transcript_original.short_description = 'Транскр.'
    transcript_translation.short_description = 'Транскр.(пер)'
    bank_document.short_description = 'Банк вып.'
    photography.short_description = 'Фото'
    anketa_embassy.short_description = 'Анкета пос.'
    zagran.short_description = 'Загран.'
    nesudimost.short_description = 'МВД'
    narko.short_description = 'Наркодисп.'
    psycho.short_description = 'Психодисп.'
    parent_permissions.short_description = 'Разр. от род.'
    bank_details.short_description = 'Рекв. банка'
    fluorography_embassy.short_description = 'Флюро'
    zagranpassport_number_id.short_description = 'Номер заграна'
    zagranpassport_end_time_admin.short_description = 'Оконч. загр.'
    nvks_custom.short_description = 'НВКС'
