from django.contrib import admin
from simqueue.models import Simulation


admin.site.register(Simulation)


from djcelery.models import TaskMeta

class TaskMetaAdmin(admin.ModelAdmin):
    readonly_fields = ('result',)
admin.site.register(TaskMeta, TaskMetaAdmin)