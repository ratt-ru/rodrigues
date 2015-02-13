from django.forms import CharField
from form_utils.forms import BetterForm


CONTAINER = 'ubuntu'



class Form(BetterForm):
    name = CharField()


    def is_valid(self):
        super(Form, self).is_valid()

        # add more form validation here