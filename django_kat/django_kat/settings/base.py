import os
from django.contrib.messages import constants as messages


BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..')

DEBUG = False
TEMPLATE_DEBUG = DEBUG


ALLOWED_HOSTS = []


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simqueue',
    'debug_toolbar.apps.DebugToolbarConfig',
    'kombu.transport.django',
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


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'simqueue.context_processors.settings',
)


ROOT_URLCONF = 'django_kat.urls'


WSGI_APPLICATION = 'django_kat.wsgi.application'


LANGUAGE_CODE = 'en-us'


TIME_ZONE = 'Africa/Johannesburg'


USE_I18N = True


USE_L10N = True


USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "static_serve")


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)


BROKER_URL = 'amqp://'
CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_BACKEND = 'amqp'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


LOGIN_REDIRECT_URL = '/'


MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.DEBUG: 'info',
    }


MEDIA_ROOT = os.path.join(BASE_DIR, 'uploaded')
MEDIA_URL = '/media/'

DOCKER_IMAGE = 'skasa/simulator'
DOCKER_CMD = './runsim.sh'
# DOCKER_CMD = 'pyxis CFG=/sims.cfg LOG=/results/output.log OUTFILE=/results/results OUTDIR=/results azishe'



LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            },
        },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
            }
    },
    }

RESULTS_DIR = os.path.join(BASE_DIR, 'results')


