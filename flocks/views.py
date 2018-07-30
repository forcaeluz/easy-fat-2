from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Flock
from farm.models import Farm


class FlockIndexView(TemplateView):

    template_name = 'flocks/index.html'

    def get_context_data(self, **kwargs):
        farm = Farm.objects.get(id=self.request.session.get('farm'))
        data = super().get_context_data(**kwargs)
        data.update({'bread_crumbs': [farm.name, 'Flocks', 'Index']})
        data.update({'farm': farm})
        data.update({'current_flocks': self.get_present_flocks()})
        data.update({'old_flocks': self.get_old_flocks()})
        return data

    def get_present_flocks(self):
        assert (self.request.session.get('farm'))
        farm_id = self.request.session.get('farm')
        return Flock.objects.present().filter(farmflockrelations__farm_id=farm_id)

    def get_old_flocks(self):
        assert (self.request.session.get('farm'))
        farm_id = self.request.session.get('farm')
        return Flock.objects.old_flocks().filter(farmflockrelations__farm_id=farm_id)

