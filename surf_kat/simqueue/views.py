from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect
from simqueue.models import Simulation
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from simqueue import tasks
from simqueue.mixins import LoginRequiredMixin


class SimulationList(ListView):
    model = Simulation


class SimulationDetail(DetailView):
    model = Simulation

class SimulationDelete(DeleteView):
    model = Simulation
    success_url = reverse_lazy('list')


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
            task = tasks.simulate.delay(simulation_id=self.object.id)
            self.object.task_id = task.task_id
            self.object.save()
            messages.info(request, 'Scheduling new task...')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class Reschedule(LoginRequiredMixin, DetailView):
    model = Simulation

    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)
        return HttpResponseRedirect(reverse('detail', args=(self.object.id,)))

    def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            self.object.log = ""
            tasks.simulate.delay(simulation_id=self.object.id)
            messages.info(request, 'Rescheduling task...')
            return HttpResponseRedirect(reverse('detail',
                                                args=(self.object.id,)))
