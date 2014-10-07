from django.forms import ModelForm
from simqueue.models import Simulation


class SimulationForm(ModelForm):
    class Meta:
        model = Simulation
        fields = '__all__'