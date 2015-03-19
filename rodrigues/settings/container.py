"""
specific config for inside container
"""

import warnings
from .base import *


SECRET_KEY = os.environ.get('SECRET_KEY')


DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'


ADMINS = (
    ('ceiling-kat admin', os.environ.get('ADMIN_EMAIL',
                                         'gijsmolenaar@gmail.com')
    ),
)


SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'gijsmolenaar@gmail.com')


TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}


BROKER_URL = 'amqp://broker/'


ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST', ['rodrigues.meqtrees.net'])]


DOCKER_URI = 'unix://var/run/docker.sock'


CYBERSKA_URI = os.environ.get('CYBERSKA_URI', '')

if not CYBERSKA_URI.strip():
    CYBERSKA_URI =  'http://%s:8081/v1/viz' % ALLOWED_HOSTS[0]


MEDIA_ROOT = '/storage/'
MEDIA_URL = '/media/'

DOCKER_SETTINGS = {
    'base_url': 'unix://var/run/docker.sock',
}


# used to determine if Django is running inside the matrix
CONTAINER = True


if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']


EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.mailgun.org')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', False)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', False)

if not EMAIL_HOST_USER:
    warnings.warn('!!! EMAIL_HOST_USER is not set !!!')

if not EMAIL_HOST_PASSWORD:
    warnings.warn('!!! EMAIL_HOST_PASSWORD is not set !!!')