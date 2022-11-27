import os
from pathlib import Path

import dj_database_url

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-s2s06pl!8)#b%!+wkfdv!s68)kj7b0(kaf-&2zyaqt=33)=x)&'

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'accounts',
    'social',
    'landing'
]


SITE_ID = 1

AUTH_USER_MODEL="accounts.User"
AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES={}


# DATABASES['default']=dj_database_url.config()

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_URL = 'static/'
# STATICFILES_DIRS=[BASE_DIR,"static"]

# STATIC_ROOT=os.path.join(BASE_DIR,"staticfiles_build/static")
STATIC_ROOT='/var/www/rycc/static'

MEDIA_URL="/media/"
MEDIA_ROOT=os.path.join(BASE_DIR,"media")



EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST ='smtp.gmail.com'
EMAIL_USE_TLS =True
EMAIL_PORT =587
EMAIL_HOST_USER ='workneedsbedone@gmail.com'
EMAIL_HOST_PASSWORD ='mtoaqfvffarpmbfy'




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL="/accounts/login/"
LOGIN_REDIRECT_URL="/"
LOGOUT_URL="/accounts/logout/"
LOGOUT_REDIRECT_URL="/"


ACCOUNT_AUTHENTICATION_METHOD ="email"
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL ="/accounts/login/"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =3
ACCOUNT_EMAIL_REQUIRED =True
ACCOUNT_EMAIL_VERIFICATION ="mandatory"
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN =150
ACCOUNT_LOGIN_ATTEMPTS_LIMIT =4
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION =True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE =True
ACCOUNT_LOGIN_ON_PASSWORD_RESET =False
ACCOUNT_SESSION_REMEMBER =True
ACCOUNT_SIGNUP_REDIRECT_URL ="/accounts/login/"
ACCOUNT_UNIQUE_EMAIL =True


CRISPY_TEMPLATE_PACK = 'bootstrap4'
