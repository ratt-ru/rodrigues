from simqueue.forms import SimulationForm
from django.views.generic.edit import FormView


class SimulationView(FormView):
    form_class = SimulationForm
