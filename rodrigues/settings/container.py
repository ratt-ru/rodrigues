"""
specific config for inside container
"""

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


ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST', 'rodrigues.meqtrees.net')]


DOCKER_URI = 'unix://var/run/docker.sock'


#CYBERSKA_URI = os.environ.get('CYBERSKA_URI', 'please set CYBERSKA_URI env var')
CYBERSKA_URI = "http://192.168.59.103:8081/v1/viz"



MEDIA_ROOT = '/storage/'
MEDIA_URL = '/media/'

DOCKER_SETTINGS = {
    'base_url': 'unix://var/run/docker.sock',
}


# used to determine if Django is running inside the matrix
CONTAINER = True


if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']