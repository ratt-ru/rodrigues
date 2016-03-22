import logging

import docker

import yaml
from kliko.django_form import generate_form
from kliko.docker import extract_params
from kliko.validate import validate_kliko

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DeleteView, DetailView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from scheduler.mixins import LoginRequiredMixin
from scheduler.models import Job, KlikoImage
from scheduler.scheduling import run_job, create_job

logger = logging.getLogger(__name__)


class ImageList(ListView):
    model = KlikoImage


class JobList(ListView):
    model = Job


class JobDelete(LoginRequiredMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('job_list')


@login_required
def schedule_image(request, image_id):
    image = KlikoImage.objects.get(pk=image_id)
    client = docker.Client(**settings.DOCKER_SETTINGS)
    params = extract_params(client, image.repository)
    parsed = yaml.load(params)
    validate_kliko(parsed)
    Form = generate_form(parsed)

    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            status, error = create_job(form, request, image=image.repository)
            if not status:
                messages.error(request, error)
            else:
                return HttpResponseRedirect(reverse('job_list'))
    else:
        form = Form()

    return render(request, 'scheduler/job_create.html', {'form': form})


class JobReschedule(LoginRequiredMixin, DetailView):
    model = Job
    success_url = reverse_lazy('job_list')

    def reschedule(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        run_job(self.object, request)
        return HttpResponseRedirect(success_url)

    # Add support for browsers which only accept GET and POST for now.
    def post(self, request, *args, **kwargs):
        return self.reschedule(request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

