from django.contrib import admin
from .models import Simulation


class TaskMetaAdmin(admin.ModelAdmin):
    readonly_fields = ('result',)

admin.site.register(Simulation)