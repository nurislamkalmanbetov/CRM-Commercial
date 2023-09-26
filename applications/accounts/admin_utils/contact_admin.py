import re

from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils.safestring import mark_safe, SafeText

from .inlines import NotificationsInline, InterviewInline
from applications.accounts.models import Profile
from applications.accounts import filters
from applications.accounts.filters import CustomDateFilter

class ProfileInContactDetailsAdmin(admin.ModelAdmin):
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
        'fishing', 'photographing',
        'study_certificate',  'study_certificate_confirm',
        'photo_for_schengen', 'photo_for_schengen_confirm',
        'zagranpassport_copy', 'zagranpassport_copy_confirm',
        'passport_copy', 'passport_copy_confirm',
        'fluorography_express', 'fluorography_express_confirm',
        'fluorography', 'fluorography_confirm',
        'immatrikulation', 'immatrikulation_confirm', 'immatrikulation_paper_confirm', 'transcript',
        'transcript_confirm', 'transcript_paper_confirm', 'bank_statement', 'bank_statement_confirm',
        'bank_statement_paper_confirm', 'conduct_certificate', 'conduct_certificate_confirm',
        'conduct_certificate_paper_confirm', 'mentaldispanser_certificate', 'mentaldispanser_certificate_confirm',
        'mentaldispanser_certificate_paper_confirm', 'drugdispanser_certificate', 'drugdispanser_certificate_confirm',
        'drugdispanser_certificate_paper_confirm', 'parental_permission', 'parental_permission_confirm',
        'parental_permission_paper_confirm', 'bank_details', 'bank_details_confirm', 'bank_details_paper_confirm',
        'contract_date', 'employer_confirm_date', 'zav_send_date', 'work_permit_date',
        'work_invitation_date', 'documents_send_date', 'local_insurance', 'german_insurance', 'accomodation', 'accomodation_type',
        'german_work_contract', 'embassy_anketa', 'transcript_translate', 'transcript_translate_confirm',
        'transcript_translate_paper_confirm', 'study_certificate_embassy', 'study_certificate_embassy_confirm',
        'study_certificate_paper_embassy_confirm', 'study_certificate_translate_embassy', 'study_certificate_translate_embassy_confirm',
        'study_certificate_translate_paper_embassy_confirm', 'documents_collected_by', 'consultant', 'consult_date',
        'flight_date', 'arrival_date', 'destination_date', 'arrival_city', 'arrival_airport', 'arrival_place',
        'marshrut', 'immatrikulation_received', 'domkom_document', 'bilet_document', 'akt_trainings', 'akt_iwex',
        'receipt_flight',
    ]

    list_display = [
        'whatsapp_link',
        'full_name_reverse',
        'nvks_custom',
        'note_form',
        'comment_form',
        'zagranpassport_number_id',
        'zagranpassport_end_time_admin',
        'university_name',
        'faculty_name',
        'year',
        'phone',
        'email',
        'bday_as_nums',
        'birth_place',
        'driver_license_admin',
        'transmission_type',
        'actual_address',
        'register_address',
        'shirt_size',
        'pants_size',
        'shoe_size',
        'father_phone',
        'father_company',
        'mother_phone',
        'mother_company',
    ]

    search_fields = [
        'user__email',
        'first_name',
        'last_name',
        'user__phone',
        'father_phone',
        'mother_phone',
        'mother_company',
        'passport_number',
        'zagranpassport_number',
    ]

    list_filter = [
        'university',
        'faculty',
        'year',
        'level',
        'shirt_size',
        'pants_size',
        'shoe_size',
        filters.DirectionFilter,
        ('bday', CustomDateFilter),
        ('study_start', CustomDateFilter),
        ('study_end', CustomDateFilter)
    ]

    change_list_template = 'admin/accounts/change_list.html'

    class Media:
        css = {
            'all': ('admin/css/changelists_custom.css',)
        }
        js = ('admin/js/changelists_custom.js',)

    def changelist_view(self, request, extra_context=None):

        if request.GET.get('get_xls', None):
            return self.export_xls(request)

        extra_context = extra_context or {}
        extra_context['table_classname'] = 'contacts'
        return super(ProfileInContactDetailsAdmin, self).changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        profile = get_object_or_404(Profile, pk=object_id)
        if profile and profile.photo:
            extra_context['photo_url'] = profile.photo.url
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def zagranpassport_number_id(self, obj, xls=False):
        return obj.zagranpassport_number

    def full_name_ru(self, obj, xls=False):
        return obj.full_name_ru

    def zagranpassport_end_time_admin(self, obj, xls=False):
        return obj.zagranpassport_end_time

    def whatsapp_link(self, obj):
        return mark_safe(f'<a href="https://api.whatsapp.com/send?phone={obj.user.whatsapp_phone}" target="_blank" title="Написать на {obj.user.whatsapp_phone}"><img src="/static/images/icons/whatsapp.svg" width="18" height="18" /></a>')

    def full_name_reverse(self, obj):
        return mark_safe(f'<a href="/admin/accounts/profileincontactdetails/{obj.id}/change?next=/admin/accounts/profileincontactdetails/" title="{obj.full_name_reverse}">{obj.full_name_reverse}</a>')

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

    def email(self, obj):
        return mark_safe(f'<a href="mailto:{obj.user.email}" target="_blank">{obj.user.email}</a>')
        
    def birth_place(self, obj):
        return f'{obj.birth_city}, {obj.birth_region} Region, {obj.birth_country}' if obj.birth_city and obj.birth_region else obj.birth_country

    def driver_license_admin(self, obj):
        str = ''
        for x in obj.get_drive_categories:
            if len(str) > 0:
                str = str + ', ' + f'{x}'
            else:
                str = str + f'{x} '
        return str

    def actual_address(self, obj):
        if obj.live_region and obj.live_city_en and obj.live_district_en and obj.live_street_en and obj.live_house and obj.live_apartment:
            return f'{obj.get_region_en(obj.live_region)}, {obj.live_city_en}, {obj.live_district_en}, {obj.live_street_en}, {obj.live_house}, {obj.live_apartment}'
        return ''

    def register_address(self, obj):
        if obj.reg_region and obj.reg_city_en and obj.reg_district_en and obj.reg_street_en and obj.reg_house and obj.reg_apartment:
            return f'{obj.get_region_en(obj.reg_region)}, {obj.reg_city_en}, {obj.reg_district_en}, {obj.reg_street_en}, {obj.reg_house}, {obj.reg_apartment}'
        return ''

    def university_name(self, obj):
        return obj.university.name if obj.university else ''

    def university_name_de(self, obj):
        return obj.university.name_de if obj.university else ''

    def university_name_ru(self, obj):
        return obj.university.name_ru if obj.university else ''

    def faculty_name(self, obj):
        return obj.faculty.name_de if obj.faculty else ''

    def faculty_name_ru(self, obj):
        return obj.faculty.name_ru if obj.faculty else ''

    def bday_as_nums(self, obj):
        return obj.bday.strftime('%d.%m.%Y') if obj.bday else ''

    def transmission_type(self, obj):
        if obj.transmission == '1':
            return 'Schaltgetriebe'
        elif obj.transmission == '2':
            return 'Automatikgetriebe'
        elif obj.transmission == '3':
            return 'Schaltgetriebe und Automatikgetriebe'
        else:
            return ''

    def shirt_size_upper(self, obj):
        return obj.shirt_size.upper()
    
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
        
        direction = request.GET.get('direction')

        if direction and direction in ['nord', 'sud']:
            queryset = queryset.filter(direction__exact=direction)

        faculty = request.GET.get('faculty__id__exact')

        if faculty and faculty.isdigit():
            queryset = queryset.filter(faculty__id=int(faculty))

        course = request.GET.get('year__exact')

        if course and course.isdigit():
            queryset = queryset.filter(year=int(course))

        level = request.GET.get('level__exact')

        if level:
            queryset = queryset.filter(level=level)

        shirt_size = request.GET.get('shirt_size__exact')

        if shirt_size:
            queryset = queryset.filter(shirt_size=shirt_size)

        pants_size = request.GET.get('pants_size__exact')

        if pants_size and pants_size.isdigit():
            queryset = queryset.filter(pants_size=int(pants_size))

        shoe_size = request.GET.get('shoe_size__exact')

        if shoe_size and shoe_size.isdigit():
            queryset = queryset.filter(shoe_size=int(shoe_size))

        strt_date = request.GET.get('bday__range__gte')
        end_date = request.GET.get('bday__range__lte')

        if strt_date and re.match('\d{2}.\d{2}.\d{4}', strt_date):
            strt_date = '-'.join(strt_date.split('.')[::-1])
            queryset = queryset.filter(bday__gte=strt_date)

        if end_date and re.match('\d{2}.\d{2}.\d{4}', end_date):
            end_date = '-'.join(end_date.split('.')[::-1])
            queryset = queryset.filter(bday__lte=end_date)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Профили")

        row_num = 0

        fields = [
            'full_name_reverse',
            'full_name_ru',
            'note',
            'comment',
            'university_name_de',
            'university_name_ru',
            'faculty_name',
            'faculty_name_ru',
            'year',
            'phone',
            'email',
            'bday_as_nums',
            'birth_place',
            'driver_license_admin',
            'transmission_type',
            'actual_address',
            'register_address',
            'shirt_size_upper',
            'pants_size',
            'shoe_size',
            'father_phone',
            'father_company',
            'mother_phone',
            'mother_company',
        ]

        # columns = []
        # model_fields = [x.name for x in Profile._meta.get_fields()]
        # for field in fields:
        #     if field in model_fields:
        #         columns.append(Profile._meta.get_field(field).verbose_name)
        #     else:
        #         columns.append(getattr(self, field).short_description)

        columns = ['Name', 'Name RU', 'Hinweis', 'Kommentar', 'Universität', 'Universität RU', 'Fakultät',
                   'Fakultät RU', 'Jahr',
                   'Telefon', 'E-Mail', 'Geburtstag', 'Geburtsort', 'Führerschein',
                   'Getriebe', 'Tatsächliche Adresse', 'Registrierungsadresse', 'Hemdgröße',
                   'Hosengröße', 'Schuhgröße', 'Vaters Telefon', 'Arbeitsort des Vaters',
                   'Mutters Telefon', 'Arbeitsplatz der Mutter']

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
                    value = '' if value is None else value
                    if type(value) != int or type(value) != float or not value:
                        value = str(value)
                    row.append(value)
                elif field == 'email':
                    row.append(obj.user.email)
                elif field == 'full_name_ru':
                    row.append(obj.full_name_ru)
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
    full_name_ru.short_description = 'Имя RU'
    note_form.short_description = 'Заметка'
    comment_form.short_description = 'Коммент.'
    phone.short_description = 'Тел.'
    email.short_description = 'Email'
    birth_place.short_description = 'Место рожд.'
    driver_license_admin.short_description = 'Вод. пр.'
    actual_address.short_description = 'Факт. адр.'
    register_address.short_description = 'Адр. проп.'
    university_name.short_description = 'Унив.'
    university_name_de.short_description = 'Унив. нем.'
    faculty_name.short_description = 'Фак.'
    bday_as_nums.short_description = 'День рождения'
    transmission_type.short_description = 'Коробка передач'
    shirt_size_upper.short_description = 'Размер рубашки'
    zagranpassport_number_id.short_description = 'Номер заграна'
    zagranpassport_end_time_admin.short_description = 'Оконч. загр.'
    nvks_custom.short_description = 'НВКС'
