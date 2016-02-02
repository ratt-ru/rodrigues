from django.contrib import admin
from .models import Job, Image


class TaskMetaAdmin(admin.ModelAdmin):
    readonly_fields = ('result',)

admin.site.register(Job)
admin.site.register(Image)