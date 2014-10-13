"""
specific config for inside container
"""

from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db_1',
        'PORT': 5432,
    }
}

BROKER_URL = 'amqp://broker_1/'
ALLOWED_HOSTS = ['127.0.0.1']

DOCKER_URI = 'unix://var/run/docker.sock'

