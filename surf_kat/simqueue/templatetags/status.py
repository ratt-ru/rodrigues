from django import template

register = template.Library()

status_trans = {
    'scheduled': 'default',
    'running': 'primary',
    'stopped': 'warning',
    'crashed': 'danger',
    'finished': 'success',
}


@register.filter
def status_label(value):
    return status_trans[value]

