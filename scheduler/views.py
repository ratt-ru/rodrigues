import pkgutil
from importlib import import_module
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView, DeleteView, CreateView
from django.http import Http404
from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse

import scheduler.forms
from .models import ScheduledContainer
from .mixins import LoginRequiredMixin
from .tasks import schedule_simulation

forms_module = scheduler.forms


def list_forms():
    return [x[1] for x in pkgutil.iter_modules(forms_module.__path__)]


class DynamicFormView(FormView):
    """
    A form view. The view is determined by the *form_name* argument. The
    corresponding form is then loaded from forms_module + <form_name>
    """
    template_name = 'form.html'
    success_url = '/admin/'

    def get_form_class(self):
        forms = list_forms()
        form = self.kwargs['form_name']
        if form not in forms:
            raise Http404

        form_module = forms_module.__name__ + "." + form
        module = import_module(form_module)
        return module.Form

    def form_valid(self, form):
        #return super(DynamicFormView, self).form_valid(form)
        import json
        return HttpResponse(json.dumps(form.cleaned_data))


class FormsList(ListView):
    template_name = "form_list.html"
    queryset = list_forms()





class SimulationList(ListView):
    model = ScheduledContainer


class SimulationDetail(DetailView):
    model = ScheduledContainer

    def get_context_data(self, **kwargs):
        context = super(SimulationDetail, self).get_context_data(**kwargs)
        #context['config'] = generate_config(self.object)
        return context




class SimulationDelete(DeleteView):
    model = ScheduledContainer
    success_url = reverse_lazy('list')


class SimulationCreate(LoginRequiredMixin, CreateView):
    model = ScheduledContainer
    success_url = reverse_lazy('list')

    def get_form_class(self):
        forms = list_forms()
        form = self.kwargs['form_name']
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
            self.object = form.save()
            self.object.save()
            schedule_simulation(self.object, request)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class Reschedule(LoginRequiredMixin, DetailView):
    model = ScheduledContainer

    def get(self, request, *args, **kwargs):
        super(Reschedule, self).get(self, request, *args, **kwargs)
        return HttpResponseRedirect(reverse('detail', args=(self.object.id,)))

    def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            self.object.clear()
            schedule_simulation(self.object, request)
            return HttpResponseRedirect(reverse('detail',
                                                args=(self.object.id,)))