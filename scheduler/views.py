import pkgutil
import json
from importlib import import_module
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView, DeleteView
from django.http import Http404
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect
import scheduler.forms
from .models import Job
from .mixins import LoginRequiredMixin
from .tasks import schedule_simulation

forms_module = scheduler.forms


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
            self.object.clear()
            schedule_simulation(self.object, request)
            return HttpResponseRedirect(reverse('job_detail',
                                                args=(self.object.id,)))