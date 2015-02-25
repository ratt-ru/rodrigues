"""
Django settings for rodrigues project.
"""


import os

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..')


SECRET_KEY = 'j@pj!2g&hp2&#c4w*h(sdq%v_j1tss%q-6x%8-k759obo_wm^4'


DEBUG = True
TEMPLATE_DEBUG = DEBUG


ALLOWED_HOSTS = []


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'scheduler',
#    'debug_toolbar.apps.DebugToolbarConfig',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

)

ROOT_URLCONF = 'rodrigues.urls'

WSGI_APPLICATION = 'rodrigues.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
}


TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'


# used to map django errors to bootstrap classes
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.DEBUG: 'info',
    }


BROKER_URL = 'amqp://localhost/'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'amqp'

RESULTS_DIR = os.path.join(BASE_DIR, 'results')