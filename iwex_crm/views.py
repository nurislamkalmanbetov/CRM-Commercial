from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from applications.core.decorators import (
    check_profile_status,
    access_to_immatrikulation_page,
    superuser_access_forbidden,
)

from applications.core.forms import (
    DocumentUploadForm,
)

from .utils import get_documents_list
from .forms import RegistrationDocumentsForm, EmbassyDocumentsForm


def main_page(request):
    return render(request, 'pages/index.html', locals())


@login_required
@superuser_access_forbidden
def personal_page(request):
    profile = request.user.profile
    notification = profile.notifications.filter(is_viewed=False).first() if profile.notifications.filter(is_viewed=False).first() else profile.notifications.first()
    return render(request, 'pages/personal_page.html', locals())


@superuser_access_forbidden
def documents_processing(request, name):
    if not request.user.is_authenticated:
        return JsonResponse(data={'code': 401, 'error': 'User is not authenticated', 'document': ''})

    profile = request.user.profile

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES, profile=profile)
        if form.is_valid():
            form.save(name)
            file = getattr(profile, name)
            url = f'/media/{file.name}' if file.name else None

            document = {
                'filename': file.name.replace(f'documents/profile_{profile.id}/', ''),
                'url': url,
            }

            data = {
                'code': 200,
                'error': '',
                'document': document,
            }

            return JsonResponse(data=data)
        return JsonResponse(data={'code': 400, 'error': 'File not upload', 'document': ''})

    if request.method == 'DELETE':
        file_field = getattr(profile, name)
        if file_field:
            file_field.delete()
            return JsonResponse(data={'code': 200, 'error': '', 'document': ''})
        return JsonResponse(data={'code': 400, 'error': 'File not found', 'document': ''})


@login_required
def documents_study_certificate(request):
    return documents_processing(request, 'study_certificate')


def documents_photo_for_schengen(request):
    return documents_processing(request, 'photo_for_schengen')


def documents_zagranpassport_copy(request):
    return documents_processing(request, 'zagranpassport_copy')


def documents_passport_copy(request):
    return documents_processing(request, 'passport_copy')


def documents_fluorography_express(request):
    return documents_processing(request, 'fluorography_express')


def documents_fluorography(request):
    return documents_processing(request, 'fluorography')


def documents_immatrikulation(request):
    return documents_processing(request, 'immatrikulation')


def documents_transcript(request):
    return documents_processing(request, 'transcript')


def documents_bank_statement(request):
    return documents_processing(request, 'bank_statement')


def documents_conduct_certificate(request):
    return documents_processing(request, 'conduct_certificate')


def documents_mentaldispanser_certificate(request):
    return documents_processing(request, 'mentaldispanser_certificate')


def documents_drugdispanser_certificate(request):
    return documents_processing(request, 'drugdispanser_certificate')


def documents_parental_permission(request):
    return documents_processing(request, 'parental_permission')


def documents_bank_details(request):
    return documents_processing(request, 'bank_details')


def documents_study_certificate_embassy(request):
    return documents_processing(request, 'study_certificate_embassy')


def documents_study_certificate_translate_embassy(request):
    return documents_processing(request, 'study_certificate_translate_embassy')


def documents_transcript_translate(request):
    return documents_processing(request, 'transcript_translate')


@login_required
@superuser_access_forbidden
@check_profile_status(['access_to_registration_documents', ], check_type=False)
def documents_registration_page(request):
    documents_list = (
        'study_certificate',
        'photo_for_schengen',
        'zagranpassport_copy',
        'passport_copy',
        'fluorography_express',
        'immatrikulation',
    )
    documents = get_documents_list(documents_list, request)

    return render(request, 'pages/documents-registration.html', locals())


@login_required
@superuser_access_forbidden
@check_profile_status(['access_to_embassy_documents', ], check_type=False)
def documents_embassy_page(request):
    documents_list = (
        'study_certificate_embassy',
        'study_certificate_translate_embassy',
        'transcript',
        'transcript_translate',
        'fluorography',
        'bank_statement',
        'conduct_certificate',
        'mentaldispanser_certificate',
        'drugdispanser_certificate',
        'parental_permission',
        'bank_details',
    )
    documents = get_documents_list(documents_list, request)
    return render(request, 'pages/documents-embassy.html', locals())


@login_required
@superuser_access_forbidden
@access_to_immatrikulation_page
@check_profile_status(['access_to_registration_documents', ], check_type=False)
def files_page(request):
    return render(request, 'pages/files.html', locals())


@login_required
@superuser_access_forbidden
def notifications_page(request):
    notifications = request.user.profile.notifications.all()
    return render(request, 'pages/notifications_page.html', locals())


@login_required
@superuser_access_forbidden
def notification_details_page(request, id):
    notification = request.user.profile.notifications.filter(id=id).first()
    if not notification.is_viewed:
        notification.is_viewed = True
        notification.save(update_fields=['is_viewed', ])

    return render(request, 'pages/notification_details_page.html', locals())


@login_required
@superuser_access_forbidden
def registration_documents_view(request):
    request_method = request.method

    if request_method == 'GET':
        form = RegistrationDocumentsForm()
        return render(request, 'pages/forms_registration_documents.html', context={'form': form})

    elif request_method == 'POST':
        bound_form = RegistrationDocumentsForm(request.POST, request.FILES, instance=request.user.profile)

        if bound_form.is_valid():
            bound_form.save()
            messages.add_message(request, messages.INFO, 'Регистрационные файлы загружены')
            return redirect(reverse('personal-page'))
        return render(request, 'pages/forms_registration_documents.html', context={'form': bound_form})


def embassy_documents_view(request):
    request_method = request.method

    if request_method == 'GET':
        form = EmbassyDocumentsForm()
        return render(request, 'pages/forms_embassy_documents.html', context={'form': form})

    elif request_method == 'POST':
        bound_form = EmbassyDocumentsForm(request.POST, request.FILES, instance=request.user.profile)

        if bound_form.is_valid():
            bound_form.save()
            messages.add_message(request, messages.INFO, 'Регистрационные файлы для посольства загружены')
            return redirect(reverse('personal-page'))
        return render(request, 'pages/forms_embassy_documents.html', context={'form': bound_form})


def error_404_page(request, exception):
    return render(request, 'pages/error_404.html')


def error_500_page(request):
    return render(request, 'pages/error_500.html')
