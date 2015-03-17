from django.conf import settings as django_settings


def settings(request):
    return {
        'CYBERSKA_URI': django_settings.CYBERSKA_URI,
        'MEDIA_ROOT': django_settings.MEDIA_ROOT,
    }
