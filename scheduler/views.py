import pkgutil
from importlib import import_module
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.http import Http404
import scheduler.forms


forms_module = scheduler.forms


def list_forms():
    return [x[1] for x in pkgutil.iter_modules(forms_module.__path__)]


class ScheduleForm(FormView):
    template_name = 'form.html'
    success_url = '/admin/'

    def get_form_class(self):
        forms = list_forms()
        form = self.kwargs['form_name']
        if not form in forms:
            raise Http404

        form_module = forms_module.__name__ + "." + form
        module = import_module(form_module)
        return module.Form

"""
    def form_valid(self, form):
        return super(ScheduleForm, self).form_valid(form)
"""

class ListForm(ListView):
    template_name = "form_list.html"
    queryset = list_forms()
