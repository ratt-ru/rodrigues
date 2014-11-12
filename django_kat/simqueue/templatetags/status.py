from django import template
import celery.states

register = template.Library()

status_trans = {
    'scheduled': 'default',
    'running': 'primary',
    'stopped': 'warning',
    'crashed': 'danger',
    'finished': 'success',
    celery.states.PENDING: 'default',
    celery.states.RECEIVED: 'primary',
    celery.states.STARTED: 'primary',
    celery.states.SUCCESS: 'success',
    celery.states.FAILURE: 'danger',
    celery.states.REVOKED: 'warning',
    celery.states.RETRY: 'warning',
}


@register.filter
def status_label(value):
    return status_trans.get(value, 'danger')



