from django import template
from scheduler.models import Job

register = template.Library()

status_trans = {
    Job.CREATED: 'default',
    Job.SCHEDULED: 'primary',
    Job.RUNNING: 'primary',
    Job.FINISHED: 'success',
    Job.CRASHED: 'danger',
}


@register.filter
def status_label(value):
    return status_trans.get(value, 'default')



