from django.contrib import admin
from datetime import date
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, FileResponse
from django.urls import path
from django.template.response import TemplateResponse

from .inlines import NotificationsInline, InterviewInline
from applications.accounts.models import Profile
from applications.common.models import SiteSettings

from applications.core.document_generators import (
    DocumentGenerator,
    BewerbungGenerator,
    ContractGenerator,
    CVGenerator,
    AnketaGenerator,
)

from applications.core.models import ContractAdmin
from applications.accounts.forms import (
    DocumentTypesForm,
    TrainingAgreementForm,
    TrainingAgreementUnchangeForm,
    AgreementActForm,
    ClosureForm,
    EmploymentDocumentsForm,
)
from django.contrib import messages


class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        NotificationsInline,
        InterviewInline,
    ]
    change_form_template = 'admin/accounts/change_form.html'

    fields = [
        'user', 'photo', 'is_confirmed', 'is_form_completed', 'is_admin_confirmed',
        'access_to_registration_documents', 'access_to_embassy_documents', 'nvks', 'start_vise_date',
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
        'work_invitation_date',
        'documents_send_date', 'local_insurance', 'german_insurance', 'accomodation', 'accomodation_type',
        'german_work_contract', 'embassy_anketa', 'transcript_translate', 'transcript_translate_confirm',
        'transcript_translate_paper_confirm', 'study_certificate_embassy', 'study_certificate_embassy_confirm',
        'study_certificate_paper_embassy_confirm', 'study_certificate_translate_embassy', 'study_certificate_translate_embassy_confirm',
        'study_certificate_translate_paper_embassy_confirm', 'documents_collected_by', 'consultant', 'full_sum', 'consult_date',
        'flight_date', 'arrival_date', 'destination_date', 'arrival_city', 'arrival_airport', 'arrival_place',
        'marshrut', 'immatrikulation_received', 'domkom_document', 'bilet_document', 'akt_trainings', 'akt_iwex',
        'receipt_flight', 'company_name', 'position', 'work_from', 'work_to', 'is_refused',
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:profile_id>/docs/', self.admin_site.admin_view(self.choose_contract)),
            path('<int:profile_id>/docs/training_agreement/', self.admin_site.admin_view(self.training_agreement)),
            path('<int:profile_id>/docs/training_stable/', self.admin_site.admin_view(self.training_unchange)),
            path('<int:profile_id>/docs/acts/', self.admin_site.admin_view(self.training_act)),
            path('<int:profile_id>/docs/closures/', self.admin_site.admin_view(self.training_close)),
            path('<int:profile_id>/docs/employment_agreement/', self.admin_site.admin_view(self.employment_agreement)),
            path('<int:profile_id>/immatrikulation/download/', self.admin_site.admin_view(self.download_immatrikulation)),
            path('<int:profile_id>/immatrikulation/print/', self.admin_site.admin_view(self.print_immatrikulation)),
            path('<int:profile_id>/jeople/download/', self.admin_site.admin_view(self.download_jeople)),
            path('<int:profile_id>/jeople/print/', self.admin_site.admin_view(self.print_jeople)),
            path('<int:profile_id>/cv/download/', self.admin_site.admin_view(self.download_cv)),
            path('<int:profile_id>/anketa/download/', self.admin_site.admin_view(self.download_anketa)),
            path('<int:profile_id>/anketa/print/', self.admin_site.admin_view(self.print_anketa)),
        ]
        return my_urls + urls

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        profile = get_object_or_404(Profile, pk=object_id)
        if profile and profile.photo:
            extra_context['photo_url'] = profile.photo.url
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def choose_contract(self, request, profile_id):
        profile = get_object_or_404(Profile, pk=profile_id)
        form = DocumentTypesForm(request.POST or None)
        context = self.admin_site.each_context(request)
        context.update({
            'profile': profile,
            'object_id': profile_id,
            'form': form,
        })

        if request.method == 'POST':
            if form.is_valid():
                document_type = form.cleaned_data.get('document_type')

                return redirect(f'/admin/accounts/profile/{profile_id}/docs/{document_type}/')
        return TemplateResponse(request, "admin/documents/choose_document.html", context)

    def training_agreement(self, request, profile_id):
        profile = get_object_or_404(Profile, pk=profile_id)
        form = TrainingAgreementForm(request.POST or None)
        context = self.admin_site.each_context(request)
        context.update({
            'profile': profile,
            'object_id': profile_id,
            'form': form,
            'contract_admins': ContractAdmin.objects.all(),
        })

        if request.method == 'POST':
            if form.is_valid():
                admin = form.cleaned_data.get('admin')
                admin = ContractAdmin.objects.filter(id=admin).first()

                agreement_cost = form.cleaned_data.get('agreement_cost')
                contract_generator = ContractGenerator(profile)

                file_path = contract_generator.generate_training_agreement(admin, agreement_cost)

                if file_path:
                    try:
                        response = FileResponse(open(file_path, 'rb'))
                        response['Content-Disposition'] = f'attachment; filename={profile.last_name}-{profile.first_name}-training-{agreement_cost.amount_in_digits}.docx'
                        update_fields = ['contract_date', 'consultant', ]
                        profile.contract_date = date.today()
                        profile.consultant = f'{admin.last_name} {admin.first_name}'

                        training_sum = agreement_cost.amount_in_digits

                        if training_sum and not profile.is_training_sum:
                            profile.training_sum = training_sum
                            profile.is_training_sum = True
                            profile.full_sum = training_sum + profile.employment_sum + profile.training_sum_stable
                            update_fields.extend(['training_sum', 'full_sum', 'is_training_sum',])

                        profile.save(update_fields=update_fields)

                        site_settings = SiteSettings.load()
                        site_settings.training_serial_number += 1

                        site_settings.save(update_fields=['training_serial_number', ])
                        return response

                    except:
                        
                        messages.add_message(request, messages.ERROR, 'Недостаточно данных для выгрузки этого документа')
                        return redirect(f'/admin/accounts/profile/{profile_id}/docs/training_agreement/')

                return redirect(f'/admin/accounts/profile/{profile_id}/docs/training_agreement/')
        return TemplateResponse(request, "admin/documents/training_agreements.html", context)

    def training_close(self, request, profile_id):
        profile = get_object_or_404(Profile, pk=profile_id)
        form = ClosureForm(request.POST or None)
        context = self.admin_site.each_context(request)
        context.update({
            'profile': profile,
            'object_id': profile_id,
            'form': form,
            'contract_admins': ContractAdmin.objects.all(),
        })

        if request.method == 'POST':
            if form.is_valid():
                admin = form.cleaned_data.get('admin')
                admin = ContractAdmin.objects.filter(id=admin).first()

                doc_type = form.cleaned_data.get('agreement_type')
                contract_generator = ContractGenerator(profile)

                if doc_type == 'training_closure':

                    if not profile.agreement1_number and not profile.agreement1_date:
                        messages.add_message(request, messages.ERROR, 'Такой договор еще не составлен')
                        return redirect(f'/admin/accounts/profile/{profile_id}/docs/closures/')

                    file_path = contract_generator.generate_close_training(admin)
                
                elif doc_type == 'employment_closure':

                    if not profile.agreement2_number and not profile.agreement2_date:
                        messages.add_message(request, messages.ERROR, 'Такой договор еще не составлен')
                        return redirect(f'/admin/accounts/profile/{profile_id}/docs/closures/')
                    
                    file_path = contract_generator.generate_close_employment()
                
                elif doc_type == 'training_stable_closure':

                    if not profile.agreement3_number and not profile.agreement3_date:
                        messages.add_message(request, messages.ERROR, 'Такой договор еще не составлен')
                        return redirect(f'/admin/accounts/profile/{profile_id}/docs/closures/')
                    
                    file_path = contract_generator.generate_close_training_stable(admin)

                if file_path:
                    try:
                        response = FileResponse(open(file_path, 'rb'))
                        response['Content-Disposition'] = f'attachment; filename={profile.last_name}-{profile.first_name}--CLOSE--.docx'
                        return response
                    except:
                        messages.add_message(request, messages.ERROR, 'Недостаточно данных для выгрузки этого документа')
                        return redirect(f'/admin/accounts/profile/{profile_id}/docs/closures/')

                return redirect(f'/admin/accounts/profile/{profile_id}/docs/closures/')
        return TemplateResponse(request, "admin/documents/choose_act.html", context)

    def training_act(self, request, profile_id):
        profile = get_object_or_404(Profile, pk=profile_id)
        form = AgreementActForm(request.POST or None)
        context = self.admin_site.each_context(request)
        context.update({
            'profile': profile,
            'object_id': profile_id,
            'form': form,
            'contract_admins': ContractAdmin.objects.all(),
        })
        if request.method == 'POST':
            if form.is_valid():

                admin = form.cleaned_data.get('admin')
                admin = ContractAdmin.objects.filter(id=admin).first()

                agreement_type = form.cleaned_data.get('agreement_type')

                contract_generator = ContractGenerator(profile)
                if agreement_type == 'training_agreement_act':

                    if not profile.agreement1_number and not profile.agreement1_date:
                        messages.add_message(request, messages.ERROR, 'Договора для этого акта не существует')
                        return redirect(f'/admin/accounts/profile/{profile_id}/docs/acts/')

                    file_path = contract_generator.generate_act_for_training(admin)

                    act_type = 'training'

                elif agreement_type == 'employment_agreement_act':

                    if not profile.agreement2_number and not profile.agreement2_date:
                        messages.add_message(request, messages.ERROR, 'Договора для этого акта не существует')
                        return redirect(f'/admin/accounts/profile/{profile_id}/docs/acts/')

                    file_path = contract_generator.generate_act_for_employment()
                    
                    act_type = 'employment'

                elif agreement_type == 'training_stable_act':

                    if not profile.agreement3_number and not profile.agreement3_date:
                        messages.add_message(request, messages.ERROR, 'Договора для этого акта не существует')
                        return redirect(f'/admin/accounts/profile/{profile_id}/docs/acts/')

                    file_path = contract_generator.generate_act_for_stable(admin)
                    
                    act_type = 'training-6000'

                if file_path:
                    try:
                        response = FileResponse(open(file_path, 'rb'))
                        response['Content-Disposition'] = f'attachment; filename={profile.last_name}-{profile.first_name}-{act_type}-act.docx'

                        return response
                    except:
                        messages.add_message(request, messages.ERROR, 'Недостаточно данных для выгрузки этого документа')
                        return redirect(f'/admin/accounts/profile/{profile_id}/docs/acts/')

                return redirect(f'/admin/accounts/profile/{profile_id}/docs/acts/')
        return TemplateResponse(request, "admin/documents/choose_act.html", context)

    def employment_agreement(self, request, profile_id):
        profile = get_object_or_404(Profile, pk=profile_id)
        form = EmploymentDocumentsForm(request.POST or None)
        context = self.admin_site.each_context(request)
        context.update({
            'profile': profile,
            'object_id': profile_id,
            'form': form,
            'contract_admins': ContractAdmin.objects.all(),
        })
        if request.method == 'POST':

            if form.is_valid():

                agreement_cost = form.cleaned_data.get('employment_document_type')
                contract_generator = ContractGenerator(profile)
                file_path = contract_generator.generate_employment_agreement(agreement_cost)

                if file_path:
                    try:
                        response = FileResponse(open(file_path, 'rb'))
                        response['Content-Disposition'] = f'attachment; filename={profile.last_name}-{profile.first_name}-employment-{agreement_cost}.docx'

                        update_fields = ['contract_date', 'consultant', ]
                        profile.contract_date = date.today()
                        employment_sum = agreement_cost

                        if employment_sum and not profile.is_employment_sum:
                            profile.employment_sum = employment_sum
                            profile.full_sum = int(employment_sum) + profile.training_sum + profile.training_sum_stable
                            profile.is_employment_sum = True
                            update_fields.extend(['employment_sum', 'is_employment_sum', 'full_sum', ])
                        profile.save(update_fields=update_fields)

                        site_settings = SiteSettings.load()
                        site_settings.employment_serial_number += 1
                        site_settings.save(update_fields=['employment_serial_number', ])

                        return response
                    except:
                        messages.add_message(request, messages.ERROR, 'Недостаточно данных для выгрузки этого документа')
                        return redirect(f'/admin/accounts/profile/{profile_id}/docs/employment_agreement/')

                return redirect(f'/admin/accounts/profile/{profile_id}/docs/employment_agreement/')
        return TemplateResponse(request, "admin/documents/employment_documents.html", context)

    def training_unchange(self, request, profile_id):
        profile = get_object_or_404(Profile, pk=profile_id)
        form = TrainingAgreementUnchangeForm(request.POST or None)
        context = self.admin_site.each_context(request)
        context.update({
            'profile': profile,
            'object_id': profile_id,
            'form': form,
            'contract_admins': ContractAdmin.objects.all(),
        })
        if request.method == 'POST':
            if form.is_valid():
                admin = form.cleaned_data.get('admin')
                admin = ContractAdmin.objects.filter(id=admin).first()

                contract_generator = ContractGenerator(profile)
                file_path = contract_generator.generate_training_unchange(admin)

                if file_path:
                    try:
                        response = FileResponse(open(file_path, 'rb'))
                        response['Content-Disposition'] = f'attachment; filename={profile.last_name}-{profile.first_name}-training-stable.docx'
                        update_fields = ['contract_date', 'consultant', ]
                        profile.contract_date = date.today()
                        profile.consultant = f'{admin.last_name} {admin.first_name}'

                        if not profile.is_training_sum_stable:
                            training_sum_stable = 6000
                            profile.training_sum = training_sum_stable
                            profile.is_training_sum_stable = True

                            profile.full_sum = training_sum_stable + profile.employment_sum + profile.training_sum_stable
                            update_fields.extend(['training_sum_stable', 'full_sum', 'is_training_sum_stable'])

                        profile.save(update_fields=update_fields)

                        site_settings = SiteSettings.load()
                        site_settings.training_serial_number += 1

                        site_settings.save(update_fields=['training_serial_number', ])
                        return response
                    except:
                        messages.add_message(request, messages.ERROR, 'Недостаточно данных для выгрузки этого документа')
                        return redirect(f'/admin/accounts/profile/{profile_id}/docs/training_stable/')

                return redirect(f'/admin/accounts/profile/{profile_id}/docs/training_stable/')
        return TemplateResponse(request, "admin/documents/training_stable_agreements.html", context)

    def download_immatrikulation(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        doc_generator = DocumentGenerator(profile)
        file = doc_generator.generate_document()
        if file:
            response = FileResponse(open(file, 'rb'))
            response['Content-Disposition'] = 'attachment; filename=' + f"{profile.last_name}-{profile.first_name}-immatrikulation-{date.today().strftime('%d-%m-%Y')}.jpg"
            return response
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    def print_immatrikulation(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        doc_generator = DocumentGenerator(profile)
        file = doc_generator.generate_pdf()
        if file:
            res = ''
            data = file.split('/')
            for x in data:
                if x == 'media':
                    res = '/'.join(data[data.index(x):])
                    break
            return redirect(f'/{res}')
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    def download_jeople(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        doc_generator = BewerbungGenerator(profile)
        file = doc_generator.generate_jeople()
        if file:
            response = FileResponse(open(file, 'rb'))
            response['Content-Disposition'] = 'attachment; filename=' + f"{profile.last_name}-{profile.first_name}-jeople-{date.today().strftime('%d-%m-%Y')}.pdf"
            return response
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    def print_jeople(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        doc_generator = BewerbungGenerator(profile)
        file = doc_generator.generate_jeople()
        if file:
            res = ''
            data = file.split('/')
            for x in data:
                if x == 'media':
                    res = '/'.join(data[data.index(x):])
                    break
            return redirect(f'/{res}')
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    def download_cv(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        doc_generator = CVGenerator(profile)
        file = doc_generator.generate_cv()
        if file:
            response = FileResponse(open(file, 'rb'))
            response['Content-Disposition'] = 'attachment; filename=' + f"{profile.last_name}-{profile.first_name}-cv-{date.today().strftime('%d-%m-%Y')}.docx"
            return response
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    def download_anketa(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        doc_generator = AnketaGenerator(profile)
        file = doc_generator.generate_anketa()
        if file:
            response = FileResponse(open(file, 'rb'))
            response['Content-Disposition'] = 'attachment; filename=' + f"{profile.last_name}-{profile.first_name}-anketa-{date.today().strftime('%d-%m-%Y')}.pdf"
            return response
        return HttpResponse('<script type="text/javascript">window.close()</script>')

    def print_anketa(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        doc_generator = AnketaGenerator(profile)
        file = doc_generator.generate_anketa()
        if file:
            res = ''
            data = file.split('/')
            for x in data:
                if x == 'media':
                    res = '/'.join(data[data.index(x):])
                    break
            return redirect(f'/{res}')
        return HttpResponse('<script type="text/javascript">window.close()</script>')
