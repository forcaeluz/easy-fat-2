from django.urls import path

from .views import FarmIndexView, NewFarmView
from buildings.views import BuildingsIndexView


app_name = 'farm'
urlpatterns = [
    path(r'', FarmIndexView.as_view(), name='index'),
    path(r'new_farm', NewFarmView.as_view(), name='new_farm'),
    path(r'buildings', BuildingsIndexView.as_view(), name='buildings'),
    path(r'dashboard/<int:farm_id>', FarmIndexView.as_view(), name='dashboard')
]