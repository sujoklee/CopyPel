"""
Django settings for forecast project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd%m137eh%#vkd#2r!xj&c+29zhehy^x5l+@htft(($3%7z8n3c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

APP_NAME = "Peleus"

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
    'django_countries',
    'forecast',
    'app',
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'forecast.urls'

# WSGI_APPLICATION = 'forecast.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'forecast.db'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TOKEN_EXPIRATION_PERIOD = 3  # set in hours
TOKEN_LENGTH = 64
DEFAULT_EMAIL = 'no-reply@peleus.com'

ORGANIZATION_TYPE = (('1', 'School'),
                     ('2', 'Think Tank'),
                     ('3', 'Company'),
                     ('4', 'Government Agency'))

FORECAST_TYPE = (('1', 'Binary'),
                 ('2', 'Probability'),
                 ('3', 'Magnitude'),
                 ('4', 'Temporal'))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# AUTH_USER_MODEL = 'app.CustomUserProfile'

# Parse database configuration from $DATABASE_URL
# import dj_database_url
#DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
# ALLOWED_HOSTS = ['*']

# Static asset configuration
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
# STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

EMAIL_TEMPLATE_FILE = 'email.html'
EMAIL_TEMPLATE_PATH = os.path.join(BASE_DIR, '..', 'app', 'templates', 'email', EMAIL_TEMPLATE_FILE)

RECAPTCHA_PUBLIC_KEY = '6Ldr5gYTAAAAAOWBFg4rtP6UKZs54wqC1Xa7t4UR'
RECAPTCHA_PRIVATE_KEY = '6Ldr5gYTAAAAAMfzv_K8zfPcdzSi1YSU2_PbvZH5'
NOCAPTCHA = True
RECAPTCHA_USE_SSL = True

