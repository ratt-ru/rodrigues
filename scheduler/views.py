import logging

import docker
import docker.errors

import yaml
import json
from kliko.django_form import generate_form
from kliko.docker import extract_params
from kliko.validate import validate_kliko

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DeleteView, CreateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms import CharField
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from rest_framework import viewsets

from .tasks import pull_image
from .models import Job, KlikoImage
from .serializers import JobSerializer, KlikoImageSerializer
from .scheduling import create_job

logger = logging.getLogger(__name__)


class ImageList(LoginRequiredMixin, ListView):
    model = KlikoImage


@method_decorator(permission_required('scheduler.create_klikoimage'), name='dispatch')
class ImageCreate(LoginRequiredMixin, CreateView):
    model = KlikoImage
    fields = ['repository', 'tag']
    success_url = reverse_lazy('image_list')


@method_decorator(permission_required('scheduler.delete_klikoimage'), name='dispatch')
class ImageDelete(LoginRequiredMixin, DeleteView):
    model = KlikoImage
    success_url = reverse_lazy('image_list')


@method_decorator(permission_required('scheduler.change_klikoimage'), name='dispatch')
class ImagePull(LoginRequiredMixin, DeleteView):
    model = KlikoImage
    success_url = reverse_lazy('image_list')
    template_name_suffix = '_pull'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        pull_image.delay(kliko_image_id=self.object.id)
        return HttpResponseRedirect(success_url)


class JobList(ListView):
    model = Job


@method_decorator(permission_required('scheduler.change_job'), name='dispatch')
class JobDelete(LoginRequiredMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('job_list')


@login_required
def schedule_image(request, image_id, template=None):
    image = KlikoImage.objects.get(pk=image_id)
    client = docker.Client(**settings.DOCKER_SETTINGS)

    if not image.available:
        raise Http404('That image is not available (yet)')

    params = extract_params(client, image.repository)
    parsed = yaml.load(params)
    validate_kliko(parsed)
    Form = generate_form(parsed)

    # inject some kliko specific fields
    Form.declared_fields['kliko_name'] = CharField(max_length=200, label='Job description')
    Form.Meta.fieldsets.append(('kliko', {'description': 'Job Parameters',
                                          'fields': ('kliko_name',)}))

    if request.method == 'POST':
        form = Form(request.POST, request.FILES)
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


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class KlikoImageViewSet(viewsets.ModelViewSet):
    queryset = KlikoImage.objects.all()
    serializer_class = KlikoImageSerializer
