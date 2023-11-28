from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi




from .views import (
    main_page,
    personal_page,
    notifications_page,
    documents_study_certificate,
    documents_photo_for_schengen,
    documents_zagranpassport_copy,
    documents_passport_copy,
    documents_fluorography_express,
    documents_fluorography,
    documents_immatrikulation,
    documents_bank_details,
    documents_parental_permission,
    documents_drugdispanser_certificate,
    documents_mentaldispanser_certificate,
    documents_conduct_certificate,
    documents_bank_statement,
    documents_transcript,
    files_page,
    notification_details_page,
    error_404_page,
    error_500_page,
    documents_registration_page,
    documents_embassy_page,
    documents_study_certificate_embassy,
    documents_study_certificate_translate_embassy,
    documents_transcript_translate,
    registration_documents_view,
    embassy_documents_view,
)

from django.views.i18n import set_language
from applications.social_auth import views



schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
#     path('', views.LoginGooglePage.as_view(), name='google'),
    path('admin/', admin.site.urls),
    path('i18n/', set_language, name='set_language'),
    path('chaining/', include('smart_selects.urls')),
    path('accounts/', include('applications.accounts.urls')),
    path('core/', include('applications.core.urls')),
    # new
    path('auth/', include('drf_social_oauth2.urls', namespace='drf_auth')),

    path('social_auth/', include(('applications.social_auth.urls', 'social_auth_app'), namespace="social_auth")),
    path('', main_page, name='main-page'),
    path('reset/', auth_views.PasswordResetView.as_view(), name='reset-password-page'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('personal/', personal_page, name='personal-page'),
    path('notifications/', notifications_page, name='notifications-page'),
    path('notifications/<id>', notification_details_page, name='notifications-page'),
    path('files/', files_page, name='files-page'),
    # TODO Delete csrf exempt
    # Documets urls
    path('documents/study_certificate/', documents_study_certificate,
         name='documents_study_certificate'),
    path('documents/photo_for_schengen/', documents_photo_for_schengen,
         name='documents_photo_for_schengen'),
    path('documents/zagranpassport_copy/', documents_zagranpassport_copy,
         name='documents_zagranpassport_copy'),
    path('documents/passport_copy/', documents_passport_copy,
         name='documents_passport_copy'),
    path('documents/fluorography_express/', documents_fluorography_express,
         name='documents_fluorography_express'),
    path('documents/fluorography/', documents_fluorography,
         name='documents_fluorography'),
    path('documents/immatrikulation/', documents_immatrikulation,
         name='documents_immatrikulation'),
    path('documents/transcript/', documents_transcript,
         name='documents_transcript'),
    path('documents/bank_statement/', documents_bank_statement,
         name='documents_bank_statement'),
    path('documents/conduct_certificate/', documents_conduct_certificate,
         name='documents_conduct_certificate'),
    path('documents/mentaldispanser_certificate/', documents_mentaldispanser_certificate,
         name='documents_mentaldispanser_certificate'),
    path('documents/drugdispanser_certificate/', documents_drugdispanser_certificate,
         name='documents_drugdispanser_certificate'),
    path('documents/parental_permission/', documents_parental_permission,
         name='documents_parental_permission'),
    path('documents/bank_details/', documents_bank_details,
         name='documents_bank_details'),
    path('documents/study_certificate_embassy/', documents_study_certificate_embassy,
          name='study_certificate_embassy'),
    path('documents/study_certificate_translate_embassy/', documents_study_certificate_translate_embassy,
          name='study_certificate_translate_embassy'),
    path('documents/transcript_translate/', documents_transcript_translate,
         name='transcript_translate'),

    # test urls for frontend
    # TODO: delete these 2 url paths after finishing frontend
    path('documents/registration-front/', documents_registration_page),
    path('documents/embassy-front/', documents_embassy_page),

    path('documents/registration/', registration_documents_view, name='documents-registration-page'),
    path('documents/embassy/', embassy_documents_view, name='documents-embassy-page'),
     re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
     path(
          "swagger/",
          schema_view.with_ui("swagger", cache_timeout=0),
          name="schema-swagger-ui",
     ),
     path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

# handler404 = error_404_page
# handler500 = error_500_page

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
                   static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)