from django.forms import CharField
from form_utils.forms import BetterForm


class Form(BetterForm):
    docker_image = 'simulation/development'

    class Meta:
        fieldsets = [('global', {'fields': ['name'],
                                 'description': 'Global settings'}),

                     ]
    name = CharField(initial='New simulation', max_length=200)
