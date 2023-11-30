"""
Django settings for iwex_crm project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from pathlib import Path
from datetime import timedelta

import django.conf.locale
from django.conf import global_settings
from .juzmin import JAZZMIN_SETTINGS, JAZZMIN_UI_TWEAKS


env = environ.Env()
environ.Env.read_env(env_file='.env')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if not DEBUG:
    sentry_sdk.init(
        dsn="https://8fb81ab3c441492f88810ffd1b861a61@sentry.io/1806921",
        integrations=[DjangoIntegration()]
    )

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'smart_selects',
    'rangefilter',

    #notifications
    'channels',

    #admin panel
    'jazzmin',

    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'easy_thumbnails',
    'storages',

    #apps
    'applications.accounts',
    'applications.core',
    'applications.common',
    'applications.social_auth',

    #backend
    'drf_yasg2',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'corsheaders',

    # excel
    'import_export',

    # translate
    'modeltranslation',

    # google auth
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',

    #3rd Party App
    'ckeditor',
    'user_visit',
]

SITE_ID = 1

AUTH_USER_MODEL = 'accounts.User'


# new
AUTHENTICATION_BACKENDS = [
   'drf_social_oauth2.backends.DjangoOAuth2',
   'django.contrib.auth.backends.ModelBackend',

    # Google  OAuth2
    'social_core.backends.google.GoogleOAuth2',
    # drf-social-oauth2
    'drf_social_oauth2.backends.DjangoOAuth2',
    # Django
    'django.contrib.auth.backends.ModelBackend',
]

# Google configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '7559994281-ql07auiv4bftm2lvir9gh28mt9rsh7j8.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

QUERYCOUNT = {
    'THRESHOLDS': {
        'MEDIUM': 50,
        'HIGH': 200,
        'MIN_TIME_TO_LOG':0,
        'MIN_QUERY_COUNT_TO_LOG':0
    },
    'IGNORE_REQUEST_PATTERNS': [],
    'IGNORE_SQL_PATTERNS': [],
    'DISPLAY_DUPLICATES': None,
    'RESPONSE_HEADER': 'X-DjangoQueryCount-Count'
}

default_app_config = 'applications.core.apps.CoreConfig'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

ASGI_APPLICATION = "iwex_crm.routing.application"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        #new
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  
        'drf_social_oauth2.authentication.SocialAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'querycount.middleware.QueryCountMiddleware',
    'user_visit.middleware.UserVisitMiddleware',   
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'iwex_crm.urls'

# new
TEMPLATE_CONTEXT_PROCESSORS = (
    'social_django.context_processors.backends',
    'social_django.context_processors.login_redirect',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                # new
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'iwex_crm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': env('POSTGRES_DB'),
#         'USER': env('POSTGRES_USER'),
#         'PASSWORD': env('POSTGRES_PASSWORD'),
#         'HOST': env('POSTGRES_HOST'),
#         'PORT': env('POSTGRES_PORT'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'iwex-crm-master6',
        'USER': 'postgres',
        'PASSWORD': 'qwerty123',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {},
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

EXTRA_LANG_INFO = {
    'ky': {
        'bidi': False,  # right-to-left
        'code': 'ky',
        'name': 'Kyrgyz',
        'name_local': 'Кыргызча', #unicode codepoints here
    },
}

JQUERY_URL = True
USE_DJANGO_JQUERY = True

DEFAULT_CHARSET = 'utf-8'


LANG_INFO = dict(django.conf.locale.LANG_INFO.items())
LANG_INFO.update(EXTRA_LANG_INFO.items())
django.conf.locale.LANG_INFO = LANG_INFO

# Languages using BiDi (right-to-left) layout
global_settings.LANGUAGES.extend([('ky', 'Кыргызча'), ])

LANGUAGE_CODE = 'en-US'

LANGUAGES = (
    ('ru', 'Russian'),
    ('de', 'German'),
    ('en', 'English'),
    ('ky', 'Kyrgyz'),
)

# LOCALE_PATHS = (
#    os.path.join(BASE_DIR, 'locale/'),
# )
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]


TIME_ZONE = 'Asia/Bishkek'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# GMAIL SMTP

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp-relay.brevo.com'
# EMAIL_HOST_PASSWORD = 'jhdSstC1Abm7WEF0'
# EMAIL_HOST_USER = 'nurislam.iwex@gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# DEFAULT_FROM_EMAIL = 'IWEX'
 
DEBUG = True #обязательно
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = 'qvfflfeokayavhnp' #c myaccount.google.com/security
EMAIL_HOST_USER = 'kalmanbetovnurislam19@gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'IWEX'

# AUTH_USER_MODEL = 'email'
# ACCOUNT_AUTHENTICATION_METHOD ="email"


JQUERY_URL = False

# Login url for @login_required decorator
LOGIN_URL = '/signin/'

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Настройки для статических файлов
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Настройки для медиа-файлов
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

CORS_ORIGIN_ALLOW_ALL = True



# settings.py
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = JAZZMIN_SETTINGS
JAZZMIN_UI_TWEAKS = JAZZMIN_UI_TWEAKS