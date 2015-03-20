"""
specific config for inside container
"""

import warnings
from .base import *


SECRET_KEY = os.environ.get('SECRET_KEY')


BROKER_URL = 'amqp://broker/'



#### Debug settings

DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'


TEMPLATE_DEBUG = DEBUG

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']



#### Database settings


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}



#### Docker settings

DOCKER_URI = 'unix://var/run/docker.sock'


DOCKER_SETTINGS = {
    'base_url': 'unix://var/run/docker.sock',
}

# used to determine if Django is running inside the matrix
CONTAINER = True



### Path settings


MEDIA_ROOT = '/storage/'
MEDIA_URL = '/media/'



#### server name settings


SERVER_NAME = os.environ.get('SERVER_NAME', 'False')

if SERVER_NAME:
    ALLOWED_HOSTS = [SERVER_NAME]
else:
    warnings.warn('!!! SERVER_NAME is not set !!!')

CYBERSKA_URI = os.environ.get('CYBERSKA_URI', '')

if not CYBERSKA_URI.strip():
    CYBERSKA_URI =  'http://%s:8081/v1/viz' % ALLOWED_HOSTS[0]



#### email settings

EMAIL_USE_TLS = True
EMAIL_PORT = 587
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', False)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.mailgun.org')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', False)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', False)

if not EMAIL_HOST_USER:
    warnings.warn('!!! EMAIL_HOST_USER is not set !!!')

if not EMAIL_HOST_PASSWORD:
    warnings.warn('!!! EMAIL_HOST_PASSWORD is not set !!!')

if not SERVER_EMAIL:
    warnings.warn('!!! SERVER_EMAIL is not set !!!')


ADMINS = (('RODRIGUES', SERVER_EMAIL),)


