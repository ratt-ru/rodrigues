from base import *

SECRET_KEY="something stupid"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

BROKER_URL = 'amqp://'


ALLOWED_HOSTS = ['127.0.0.1']

