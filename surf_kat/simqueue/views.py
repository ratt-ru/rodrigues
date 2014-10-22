from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect
from simqueue.models import Simulation
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib import messages
from simqueue import tasks
from simqueue.mixins import LoginRequiredMixin
from .config import generate_config


fields = (
    'name',
    'sky_type',
    'sky_model',
    'tdl_conf',
    'tdl_section',
    'make_psf',
    'add_noise',
    'vis_noise_std',
    'output',
    'ms_hours',
    'ms_dtime',
    'ms_freq0',
    'ms_dfreq',
    'ms_nchan',
    'ms_nband',
    'ms_write_auto_corr',
    'ms_dec',
    'ms_ra',
    'ds_amp_phase_gains',
    'ds_parallactic_angle_rotation',
    'ds_primary_beam',
    'ds_feed_angle',
    'cr_amp_phase_gains',
    'cr_pointing_error',
    'cr_rfi',
    'im_npix',
    'im_cellsize',
    'im_weight',
    'im_weight_fov',
    'im_wprojplanes',
    'im_mode',
    'im_spwid',
    'channelise',
    'im_stokes',
    'deconvolve',
    'dc_operation',
    'dc_uservector',
    'dc_nscales',
    'dc_niter',
    'dc_threshold',
)


class SimulationList(ListView):
    model = Simulation


class SimulationDetail(DetailView):
    model = Simulation

    def get_context_data(self, **kwargs):
        context = super(SimulationDetail, self).get_context_data(**kwargs)
        context['config'] = generate_config(self.object)
        return context


class SimulationConfig(DetailView):
    model = Simulation
    template_name = 'simqueue/config.txt'
    content_type = 'text/plain'


class SimulationDelete(DeleteView):
    model = Simulation
    success_url = reverse_lazy('list')


class SimulationCreate(LoginRequiredMixin, CreateView):
    model = Simulation
    fields = fields
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



