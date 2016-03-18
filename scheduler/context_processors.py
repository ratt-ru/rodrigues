from django.conf import settings as django_settings


def settings(request):
    return {
        'MEDIA_ROOT': django_settings.MEDIA_ROOT,
    }
