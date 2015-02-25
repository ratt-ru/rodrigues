from django.contrib import admin
from .models import Job


class TaskMetaAdmin(admin.ModelAdmin):
    readonly_fields = ('result',)

admin.site.register(Job)