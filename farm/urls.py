from django.conf.urls import url

from .views import FarmIndexView, NewFarmView
from buildings.views import BuildingsIndexView


app_name = 'farm'
urlpatterns = [
    url(r'^$', FarmIndexView.as_view(), name='index'),
    url(r'^new_farm$', NewFarmView.as_view(), name='new_farm'),
    url(r'^buildings$', BuildingsIndexView.as_view(), name='buildings')
]