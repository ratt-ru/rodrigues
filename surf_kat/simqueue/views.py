from django.core.urlresolvers import reverse_lazy
from simqueue.models import Simulation
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.contrib import messages
from simqueue import tasks
from simqueue.mixins import LoginRequiredMixin


class SimulationList(ListView):
    model = Simulation


class SimulationDetail(DetailView):
    model = Simulation


class SimulationCreate(LoginRequiredMixin, CreateView):
    model = Simulation
    fields = '__all__'
    success_url = reverse_lazy('list')

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.object = form.save()
            tasks.simulate.delay(simulation_id=self.object.id)
            messages.info(request, 'Scheduling new task...')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
