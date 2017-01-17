"""
specific config for inside container
"""

import warnings
from .base import *


SECRET_KEY = os.environ.get('SECRET_KEY')


BROKER_URL = 'amqp://broker/'


#### Debug settings

DEBUG = os.environ.get('DEBUG', 'false').lower() in ('true', 'on')
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG


if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware']


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


# used to determine if Django is running inside the matrix
CONTAINER = True



### Path settings


MEDIA_ROOT = '/storage/'
MEDIA_URL = '/media/'

# NOTE: this should be the path to storage on the HOST, not inside the container
HOST_STORAGE = os.environ.get('STORAGE')


#### server name settings

SERVER_NAME = os.environ.get('SERVER_NAME', False)

if not SERVER_NAME:
    SERVER_NAME = 'rodrigues.meqtrees.net'
    warnings.warn('!!! SERVER_NAME is not set, using rodrigues.meqtrees.net !!!')

ALLOWED_HOSTS = [SERVER_NAME]


#### email settings

EMAIL_USE_TLS = True
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', False) or '587')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', False)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.mailgun.org')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', False)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', False)
ADMINS = (('Rodrigues Calibratori', SERVER_EMAIL),)


#### show the settings

print("******* RODRIGUES SETTINGS *******")
for v in ['DEBUG', 'SERVER_NAME', 'ALLOWED_HOSTS', 'SECRET_KEY',
            'SERVER_EMAIL', 'EMAIL_HOST', 'EMAIL_HOST_USER',
            'EMAIL_HOST_PASSWORD', 'HOST_STORAGE']:
    print("%s:\t%s" % (v, str(globals().get(v, 'not set'))))



