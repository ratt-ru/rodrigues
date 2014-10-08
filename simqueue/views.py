
from simqueue.forms import SimulationForm
from django.views.generic.edit import FormView
from simqueue import tasks


class SimulationView(FormView):
    form_class = SimulationForm

    def form_valid(self, form):
        tasks.simulate.delay()
        return super(SimulationView, self).form_valid(form)