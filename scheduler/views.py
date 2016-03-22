import logging

import docker

import yaml
import json
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
def schedule_image(request, image_id, template=None):
    image = KlikoImage.objects.get(pk=image_id)
    client = docker.Client(**settings.DOCKER_SETTINGS)
    params = extract_params(client, image.repository)
    parsed = yaml.load(params)
    validate_kliko(parsed)
    Form = generate_form(parsed)

    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            status, error = create_job(form, request, image=image)
            if not status:
                messages.error(request, error)
            else:
                return HttpResponseRedirect(reverse('job_list'))
    else:
        if template:
            form = Form(template)
        else:
            form = Form()

    return render(request, 'scheduler/job_create.html', {'form': form})


@login_required
def reschedule_image(request, template_job_id):
    job = Job.objects.get(pk=template_job_id)
    template = json.loads(job.config)
    return schedule_image(request, job.image.id, template)
