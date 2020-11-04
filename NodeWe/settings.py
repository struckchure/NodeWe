"""
Django settings for NodeWe project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0qbiz@v46kx&ut19(v^edq$f0$fu(^_ci4(5#-ofh#%b%kvwh@'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False

ALLOWED_HOSTS = [
    '139.162.211.200',
    'nodewe.com',
    'www.nodewe.com',
    'localhost'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'Home.apps.HomeConfig',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # Custom middleware
    'Home.middleware.WwwRedirectMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'NodeWe.urls'

AUTHENTICATION_BACKENDS = ( 
    'django.contrib.auth.backends.ModelBackend', 
    'allauth.account.auth_backends.AuthenticationBackend', 
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'NodeWe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'Home.User'
LOGIN_URL = 'Home:login'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ameenem2702@gmail.com'
EMAIL_HOST_PASSWORD = 'zxcjjdsgntltyfsb'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, f'static')
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'Media')
MEDIA_URL = '/Media/'

####################
# APIs Credentials #
####################


ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400 
LOGIN_REDIRECT_URL = 'Home:dashboard'
ACCOUNT_LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL

SITE_ID = 1


# GitHub

GITHUB_CLIENT_KEY = 'f52e2612b300fec45817'
GITHUB_CLIENT_SECRET = '0def268f8db9e5f4c772f97fcaeeb766a6bf5f0b'

# Facebook

FACEBOOK_CLIENT_ID = 657502841632941
FACEBOOK_CLIENT_SECRET = 'd26b0dd263f4c02df412e75a845c18d6'

# Google

GOOGLE_CLIENT_ID = '890326707410-ubro1cpvggfjoen5k4vdh3bacs4bj89o.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '4Myyots_QCMhF3NbSkqMuWrV'
