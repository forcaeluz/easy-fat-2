from django.forms import ModelForm, BaseFormSet

from easyfat_ui.forms import EasyFatForm
from .models import Farm

from buildings.models import AnimalRoomEntry


class NewFarmForm(EasyFatForm, ModelForm):

    title = 'New Farm'

    class Meta:
        model = Farm
        exclude = []


class FarmAnimalEntryRoomInformation(EasyFatForm, ModelForm):
    class Meta:
        model = AnimalRoomEntry
        exclude = ['date']
