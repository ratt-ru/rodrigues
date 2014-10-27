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
    'djcelery',
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


ROOT_URLCONF = 'surf_kat.urls'


WSGI_APPLICATION = 'surf_kat.wsgi.application'


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


CELERY_ACCEPT_CONTENT = ['pickle', 'json']


CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'


LOGIN_REDIRECT_URL = '/'


MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.DEBUG: 'info',
}



DOCKER_IMAGE = 'gijzelaerr/ceiling-kat'
DOCKER_CMD = 'sh -c "' \
             'cd /opt/ceiling-kat/web-kat && ' \
             'pyxis ' \
             'CFG=/results/sims.cfg ' \
             'LOG=/results/output.log ' \
             'OUTFILE=/results/results ' \
             'OUTDIR=/results azishe"'

