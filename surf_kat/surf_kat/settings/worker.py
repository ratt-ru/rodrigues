from .base import *

SECRET_KEY = 'doesntmatter'

DEBUG = False



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