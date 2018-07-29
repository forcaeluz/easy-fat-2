from django.forms import ModelForm
from easyfat_ui.forms import EasyFatForm

from .models import AnimalFlockExit, AnimalFarmExit, Flock


class FlockEntryForm(EasyFatForm, ModelForm):

    class Meta:
        model = Flock
        exclude = []
