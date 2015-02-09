from django.conf import settings as django_settings


def settings(request):
    return {
        'CYBERSKA_URI': django_settings.CYBERSKA_URI
    }
