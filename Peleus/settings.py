"""
Django settings for Peleus project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3k5h20ji8$_f^iycfc$1g#s2b%fwd7q2fby@(r8m+9s6^4zr0a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

APPEND_SLASH = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

APP_NAME = "Peleus"


# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
    'django_countries',
    # 'bootstrapform',
    'forecast',
    'taggit'
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Peleus.urls'

WSGI_APPLICATION = 'Peleus.wsgi.application'

LOGIN_REDIRECT_URL = '/'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    # 'default': {
    # 'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'peleus',
    #     'USER': 'peleus',
    #     'PASSWORD': 'WeakPassw0rd!',
    #     'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
    #     'PORT': '3306',
    # }
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': ("django.contrib.auth.context_processors.auth",
                                           "forecast.context_processors.forecast_user",
                                           "forecast.context_processors.forecast_interests",
                                           "django.template.context_processors.debug",
                                           "django.template.context_processors.i18n",
                                           "django.template.context_processors.media",
                                           "django.template.context_processors.static",
                                           "django.template.context_processors.tz",
                                           "django.contrib.messages.context_processors.messages")},
        'DIRS': (os.path.join(BASE_DIR, 'templates'),)
    },
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'forecast', 'static', 'media')
MEDIA_URL = '/media/'

RECAPTCHA_PUBLIC_KEY = '6Ldr5gYTAAAAAOWBFg4rtP6UKZs54wqC1Xa7t4UR'
RECAPTCHA_PRIVATE_KEY = '6Ldr5gYTAAAAAMfzv_K8zfPcdzSi1YSU2_PbvZH5'
NOCAPTCHA = True
RECAPTCHA_USE_SSL = True

TOKEN_EXPIRATION_PERIOD = 5  # set in hours
TOKEN_LENGTH = 64

DEFAULT_EMAIL = 'no-reply@peleus.com'
EMAIL_SERVER = 'smtp.gmail.com:587'
EMAIL_USER = 'Peleus.key@gmail.com'
EMAIL_PASSWORD = 'Castle12!21'
_EMAIL_TEMPLATE_FILE = 'email.html'
EMAIL_TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates', 'email', _EMAIL_TEMPLATE_FILE)

ORGANIZATION_TYPE = (('1', 'School'),
                     ('2', 'Think Tank'),
                     ('3', 'Company'),
                     ('4', 'Government Agency'))

FORECAST_TYPE = ((u'1', 'Binary'),
                 (u'2', 'Probability'),
                 (u'3', 'Magnitude'),
                 (u'4', 'Temporal'))

AREAS = (('1', "Elections"),
         ('2', "Conflicts/Wars"),
         ('3', "Social Events/Protests"),
         ('4', "Fiscal and Monetary Actions"),
         ('5', "Inter-State Negotiations"),
         ('6', "Trade Agreements"),
         ('7', "Private Sector Engagements"))

REGIONS = (('1', "Europe"),
           ('2', "Middle East"),
           ('3', "Africa"),
           ('4', "Asia"),
           ('5', "South Pacific"),
           ('6', "North America"),
           ('7', "South America"))

STATUS_CHOICES = (('u', "Unpublished"),
                  ('p', "Published"))

FORECAST_FILTER_MOST_ACTIVE = "mostactive"
FORECAST_FILTER_NEWEST = "newest"
FORECAST_FILTER_CLOSING = "closing"

FORECAST_FILTERS = {FORECAST_FILTER_MOST_ACTIVE, FORECAST_FILTER_NEWEST, FORECAST_FILTER_CLOSING}

DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'

DOMAIN_NAME = 'http://localhost:8000'   # change this in production
