from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from applications.accounts.models import Profile
from .inlines import NotificationsInline, InterviewInline
from django.utils.safestring import mark_safe, SafeText


class ProfileInArchiveAdmin(admin.ModelAdmin):
    inlines = [
        NotificationsInline,
        InterviewInline,
    ]

    fields = [
        'user', 'photo', 'is_confirmed', 'is_form_completed', 'is_admin_confirmed',
        'access_to_registration_documents', 'access_to_embassy_documents', 'start_vise_date',
        'end_vise_date', 'level', 'courses_info', 'first_name', 'first_name_ru', 'last_name',
        'last_name_ru', 'gender', 'bday', 'nationality', 'birth_country', 'birth_region',
        'birth_city', 'reg_region', 'reg_city', 'reg_city_en', 'reg_district', 'reg_district_en',
        'reg_street', 'reg_street_en', 'reg_house', 'reg_apartment', 'live_region', 'live_city',
        'live_city_en', 'live_district', 'live_district_en', 'live_street', 'live_street_en', 'live_house',
        'live_apartment', 'passport_number', 'zagranpassport_number', 'zagranpassport_end_time', 'embassy_visametric',
        'termin', 'university', 'faculty', 'degree', 'year',
        'study_start', 'study_end', 'summer_holidays_start', 'summer_holidays_end', 'father_phone', 'father_work_phone',
        'father_company', 'mother_phone', 'mother_work_phone', 'mother_company', 'company1', 'position1', 'start_date1',
        'end_date1', 'country1', 'company2', 'position2', 'start_date2', 'end_date2', 'country2', 'company3',
        'position3', 'start_date3', 'end_date3', 'country3', 'german', 'english', 'turkish', 'russian', 'chinese',
        'driver_license', 'driving_experience', 'cat_a', 'cat_b', 'cat_c', 'cat_d', 'cat_e', 'tractor',
        'transmission', 'bicycle_skill', 'shirt_size', 'pants_size', 'shoe_size', 'reading', 'singing', 'travelling',
        'yoga', 'dancing', 'sport', 'drawing', 'computer_games', 'guitar', 'films', 'music', 'knitting', 'cooking',
        'fishing', 'photographing', 'study_certificate', 'study_certificate_confirm', 'study_certificate_paper_confirm',
        'photo_for_schengen', 'photo_for_schengen_confirm', 'photo_for_schengen_paper_confirm', 'zagranpassport_copy',
        'zagranpassport_copy_confirm', 'zagranpassport_copy_paper_confirm', 'passport_copy', 'passport_copy_confirm',
        'passport_copy_paper_confirm', 'fluorography_express', 'fluorography_express_confirm',
        'fluorography_express_paper_confirm', 'fluorography', 'fluorography_confirm', 'fluorography_paper_confirm',
        'immatrikulation', 'immatrikulation_confirm', 'immatrikulation_paper_confirm', 'transcript',
        'transcript_confirm', 'transcript_paper_confirm', 'bank_statement', 'bank_statement_confirm',
        'bank_statement_paper_confirm', 'conduct_certificate', 'conduct_certificate_confirm',
        'conduct_certificate_paper_confirm', 'mentaldispanser_certificate', 'mentaldispanser_certificate_confirm',
        'mentaldispanser_certificate_paper_confirm', 'drugdispanser_certificate', 'drugdispanser_certificate_confirm',
        'drugdispanser_certificate_paper_confirm', 'parental_permission', 'parental_permission_confirm',
        'parental_permission_paper_confirm', 'bank_details', 'bank_details_confirm', 'bank_details_paper_confirm',
        'jipl_paper_confirm', 'resume_paper_confirm', 'work_contract_paper_confirm', 'traning_contract_paper_confirm',
        'receipt_paper_confirm', 'contract_date',  'employer_confirm_date', 'zav_send_date', 'work_permit_date',
        'work_invitation_date', 'documents_send_date', 'local_insurance', 'german_insurance', 'accomodation', 'accomodation_type',
        'german_work_contract', 'embassy_anketa', 'transcript_translate', 'transcript_translate_confirm',
        'transcript_translate_paper_confirm', 'study_certificate_embassy', 'study_certificate_embassy_confirm',
        'study_certificate_paper_embassy_confirm', 'study_certificate_translate_embassy', 'study_certificate_translate_embassy_confirm',
        'study_certificate_translate_paper_embassy_confirm', 'documents_collected_by', 'consultant', 'consult_date',
        'flight_date', 'arrival_date', 'destination_date', 'arrival_city', 'arrival_airport', 'arrival_place',
        'marshrut', 'immatrikulation_received', 'domkom_document', 'bilet_document', 'akt_trainings', 'akt_iwex',
        'receipt_flight',
    ]

    search_fields = [
        'first_name',
        'last_name',
        'user__phone',
        'passport_number',
        'zagranpassport_number',
    ]

    list_display = [
        'whatsapp_link',
        'full_name_reverse',
        'zagranpassport_number_id',
        'zagranpassport_end_time_admin',
        'university',
        'faculty',
        'year',
        'phone',
        'note_form',
        'comment_form',
    ]

    change_list_template = 'admin/accounts/change_list.html'

    class Media:
        css = {
            'all': ('admin/css/changelists_custom.css',)
        }
        js = ('admin/js/changelists_custom.js',)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        profile = get_object_or_404(Profile, pk=object_id)
        if profile and profile.photo:
            extra_context['photo_url'] = profile.photo.url
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def whatsapp_link(self, obj):
        return mark_safe(f'<a href="https://api.whatsapp.com/send?phone={obj.user.whatsapp_phone}" target="_blank" title="Написать на {obj.user.whatsapp_phone}"><img src="/static/images/icons/whatsapp.svg" width="18" height="18" /></a>')

    def zagranpassport_number_id(self, obj, xls=False):
        return obj.zagranpassport_number

    def zagranpassport_end_time_admin(self, obj, xls=False):
        return obj.zagranpassport_end_time

    def full_name_reverse(self, obj):
        return mark_safe(f'<a href="/admin/accounts/profile/{obj.id}/change?next=/admin/accounts/profilenotconfirmed/" title="{obj.full_name_reverse}">{obj.full_name_reverse}</a>')

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

    def export_xls(self, request):
        import xlwt

        queryset = self.get_queryset(request=request).order_by('last_name', 'first_name')
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Профили")

        row_num = 0

        fields = [
            'full_name_reverse',
            'university',
            'faculty',
            'year',
            'phone',
            'note',
            'comment',
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
    comment_form.short_description = 'Комментарии'
    phone.short_description = 'Номер'
    zagranpassport_number_id.short_description = 'Номер заграна'
    zagranpassport_end_time_admin.short_description = 'Оконч. загр.'
