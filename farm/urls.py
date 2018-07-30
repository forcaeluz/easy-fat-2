from django.urls import path

from .views import FarmIndexView, NewFarmView
from .wizards import NewAnimalEntryWizard
from buildings.views import BuildingsIndexView
from flocks.views import FlockIndexView


app_name = 'farm'
urlpatterns = [
    path(r'', FarmIndexView.as_view(), name='index'),
    path(r'new_farm', NewFarmView.as_view(), name='new_farm'),
    path(r'buildings', BuildingsIndexView.as_view(), name='buildings'),
    path(r'flocks', FlockIndexView.as_view(), name='flocks'),
    path(r'dashboard/<int:farm_id>', FarmIndexView.as_view(), name='dashboard'),
    path(r'new_animal_entry', NewAnimalEntryWizard.as_view(), name='new_animal_entry')
]