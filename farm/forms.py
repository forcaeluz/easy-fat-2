from django.forms import ModelForm

from easyfat_ui.forms import EasyFatForm
from .models import Farm


class NewFarmForm(EasyFatForm, ModelForm):

    title = 'New Farm'

    class Meta:
        model = Farm
        exclude = []
