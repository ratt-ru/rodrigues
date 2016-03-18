from .base import *
from docker.utils import kwargs_from_env


DOCKER_SETTINGS = kwargs_from_env()

# required foor boot2docker
if 'tls' in DOCKER_SETTINGS:
    DOCKER_SETTINGS['tls'].assert_hostname = False


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


DOCKER_URI = 'tcp://192.168.59.103:2375'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'