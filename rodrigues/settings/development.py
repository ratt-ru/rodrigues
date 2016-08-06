from .base import *
from docker.utils import kwargs_from_env


SECRET_KEY = "something stupid"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS += [
    'debug_toolbar',
]


BROKER_URL = 'amqp://localhost/'


ALLOWED_HOSTS = ['127.0.0.1']


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# outside a container the host storage is the same as media_root
HOST_STORAGE = MEDIA_ROOT

CORS_ORIGIN_ALLOW_ALL = True