"""
specific config for inside container
"""

from .base import *


SECRET_KEY = os.environ.get('SECRET_KEY')


DEBUG = False


ADMINS = (
    ('ceiling-kat admin', os.environ.get('ADMIN_EMAIL', 'gijsmolenaar@gmail.com')),
)

EMAIL_HOST = 'mail'


SERVER_EMAIL = 'gijsmolenaar@gmail.com'


if os.environ.get('DEBUG', 'false').lower() == 'true':
    DEBUG = True

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

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST', 'ceiling-kat.meqtrees.net')]

DOCKER_URI = 'unix://var/run/docker.sock'


# Set your DSN value
RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN', 'please set SENTRY_DSN in fig.yml'),
}

# Add raven to the list of installed apps
INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
)


CYBERSKA_URL = os.environ.get('CYBERSKA_URL', 'please set CYBERSKA_URL in fig.yml')