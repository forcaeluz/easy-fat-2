from django.utils.translation import gettext as _
from django.forms import ModelForm


from easyfat_ui.forms import EasyFatForm

from .models import Building, RoomGroup, Room


class BuildingForm(ModelForm, EasyFatForm):
    title = _('New Building')

    class Meta:
        model = Building
        exclude = ['group']


class RoomGroupForm(ModelForm, EasyFatForm):
    title = _('New Room Group')

    class Meta:
        model = RoomGroup
        exclude = []


class RoomForm(ModelForm, EasyFatForm):
    title = _('New Room')

    class Meta:
        model = Room
        exclude = []
