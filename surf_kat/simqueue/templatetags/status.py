from django import template

register = template.Library()

status_trans = {
    'scheduled': 'default',
    'running': 'primary',
    'stopped': 'warning',
    'crashed': 'danger',
    'finished': 'success',
}

alert_trans = {
    'debug': 'info',
    'info':  'info',
    'success': 'succes',
    'warning': 'warning',
    'error': 'danger',
}


@register.filter
def status_label(value):
    return status_trans[value]


@register.filter
def alert_label(value):
    return alert_trans[value]
