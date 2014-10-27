from django.contrib import admin
from simqueue.models import Simulation
from djcelery.models import TaskMeta


class TaskMetaAdmin(admin.ModelAdmin):
    readonly_fields = ('result',)


#admin.site.register(TaskMeta, TaskMetaAdmin)
admin.site.register(Simulation)