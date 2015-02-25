from django import template
from celery import states

register = template.Library()

status_trans = {
    states.PENDING: 'default',
    states.RECEIVED: 'primary',
    states.STARTED: 'primary',
    states.SUCCESS: 'success',
    states.FAILURE: 'danger',
    states.REVOKED: 'warning',
    states.RETRY: 'warning',
}


@register.filter
def status_label(value):
    return status_trans.get(value, 'danger')



