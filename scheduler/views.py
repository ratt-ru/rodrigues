import pkgutil
import json
from importlib import import_module
import socket
import logging

from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic import ListView, DeleteView
from django.http import Http404
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect

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
        job.state = job.CRASHED
        error = "can't connect to broker %s: %s" % (job.id,
                                                   str(e))
        messages.error(request, error)
        logger.error(error)
        job.log = error
    else:
        job.task_id = async.task_id
        job.state = job.SCHEDULED
    job.save()


def list_forms():
    return [x[1] for x in pkgutil.iter_modules(forms_module.__path__)]


class FormsList(LoginRequiredMixin, ListView):
    template_name = "scheduler/form_list.html"
    queryset = list_forms()


class JobList(ListView):
    model = Job


class JobDelete(LoginRequiredMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('job_list')


class JobCreate(LoginRequiredMixin, FormView):
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
            self.object.owner = request.user
            self.object.config = json.dumps(form.cleaned_data)
            self.object.name = form.data['name']
            self.object.docker_image = form.docker_image
            self.object.save()
            schedule_simulation(self.object, request)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class JobReschedule(LoginRequiredMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('job_list')

    def reschedule(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        schedule_simulation(self.object, request)
        return HttpResponseRedirect(success_url)

    # Add support for browsers which only accept GET and POST for now.
    def post(self, request, *args, **kwargs):
        return self.reschedule(request, *args, **kwargs)

