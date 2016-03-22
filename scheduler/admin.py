from django.contrib import admin
from .models import Job, KlikoImage
from .tasks import pull_image


def pull(modeladmin, request, queryset):
    for image in queryset:
        pull_image.delay(kliko_image_id=image.id)
pull.short_description = 'Pull selected images from Docker hub'



@admin.register(KlikoImage)
class KlikoImageAdmin(admin.ModelAdmin):
    list_display = ('repository', 'tag', 'state', 'last_updated', 'error_message')
    readonly_fields = ('state', 'last_updated', 'error_message')
    actions = [pull]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass
