from django.conf import settings as django_settings


def settings(request):
    return {
        'CYBERSKA_URL': django_settings.CYBERSKA_URL
    }
