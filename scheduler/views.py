import pkgutil
import json
from importlib import import_module
import socket
import logging
import os

from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView, DeleteView, View
from django.http import Http404
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings

import matplotlib
import aplpy

import scheduler.forms
from scheduler.models import Job
from scheduler.mixins import LoginRequiredMixin
from scheduler.tasks import simulate


logger = logging.getLogger(__name__)


forms_module = scheduler.forms


def schedule_simulation(job, request):
    """
    schedule a simulation task, catch error if problem, log in all cases.
    """
    try:
        async = simulate.delay(job_id=job.id)
    except (OSError, socket.error) as e:
        error = "can't start simulation %s: %s" % (job.id,
                                                   str(e))
        messages.error(request, error)
        logger.error(error)
        job.log = error
        job.save()
    else:
        job.task_id = async.task_id
        job.save(update_fields=["task_id"])
        job.set_scheduled()


def list_forms():
    return [x[1] for x in pkgutil.iter_modules(forms_module.__path__)]


class FormsList(ListView):
    template_name = "scheduler/form_list.html"
    queryset = list_forms()


class JobList(ListView):
    model = Job


class JobDetail(DetailView):
    model = Job


class JobDelete(DeleteView):
    model = Job
    success_url = reverse_lazy('job_list')


class JobCreate(FormView, LoginRequiredMixin):
    model = Job
    success_url = reverse_lazy('job_list')
    template_name = 'scheduler/job_create.html'

    def get_form_class(self):
        forms = list_forms()
        form = self.kwargs['form']
        if form not in forms:
            raise Http404

        form_module = forms_module.__name__ + "." + form
        module = import_module(form_module)
        return module.Form

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.object = Job()
            self.object.config = json.dumps(form.cleaned_data)
            self.object.name = form.data['name']
            self.object.docker_image = form.docker_image
            self.object.save()
            schedule_simulation(self.object, request)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class JobReschedule(LoginRequiredMixin, DetailView):
    model = Job

    def get(self, request, *args, **kwargs):
        super(JobReschedule, self).get(self, request, *args, **kwargs)
        return HttpResponseRedirect(reverse('job_detail',
                                            args=(self.object.id,)))

    def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            schedule_simulation(self.object, request)
            return HttpResponseRedirect(reverse('job_detail',
                                                args=(self.object.id,)))


class FitsView(View):
    """
    Returns an rendered image. uses path keyword argument. Only
    allowes files which are in te settings.RESULTS_DIR folder somewhere.
    """
    def render_to_response(self, context, **kwargs):
        path = self.kwargs['path']
        fullpath = os.path.realpath(os.path.join(settings.RESULTS_DIR, path))
        if not fullpath.startswith(settings.RESULTS_DIR):
            raise Http404
        if not os.access(fullpath, os.R_OK):
            raise Http404
        response = HttpResponse(content_type='image/png')
        fig = matplotlib.pyplot.figure()

        try:
            plot = aplpy.FITSFigure(fullpath, figure=fig,
                                    auto_refresh=False)
        except IOError as e:
            matplotlib.pyplot.text(0.1, 0.8, str(e))
        else:
            plot.show_colorscale()
        fig.canvas.print_figure(response, format='png')
        return response

