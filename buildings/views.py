from django.views.generic import TemplateView
from django.views.generic import ListView, FormView
from django.urls.base import reverse_lazy

from easyfat_ui.views import EasyFatFormView
from farm.models import Farm
from .models import Building, RoomGroup

from .forms import BuildingForm, RoomGroupForm, RoomForm


class BuildingView(TemplateView):

    template_name = 'buildings/index.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class BuildingsIndexView(ListView):
    def get_queryset(self):
        assert(self.request.session.get('farm'))
        farm_id = self.request.session.get('farm')
        return Building.objects.filter(farmbuildingrelations__farm_id=farm_id)

    template_name = 'buildings/index.html'
    model = Building

    def get_context_data(self, **kwargs):
        farm = Farm.objects.get(id=self.request.session.get('farm'))
        data = super().get_context_data(**kwargs)
        data.update({'bread_crumbs': [farm.name, 'Buildings', 'Index']})
        data.update({'farm': farm})
        return data


class NewBuildingView(EasyFatFormView):

    form_class = BuildingForm
    success_url = reverse_lazy('buildings:index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class NewRoomGroupView(EasyFatFormView):

    form_class = RoomGroupForm
    success_url = reverse_lazy('buildings:index')

    def get_form_kwargs(self):
        kwargs_dict = super().get_form_kwargs()
        if self.request.GET.get('group'):
            kwargs_dict.update({'initial': {'group': RoomGroup.objects.get(id=self.request.GET.get('group'))}})
            print(kwargs_dict)
        return kwargs_dict

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class NewRoomView(EasyFatFormView):

    form_class = RoomForm
    success_url = reverse_lazy('buildings:index')

    def get_form_kwargs(self):
        kwargs_dict = super().get_form_kwargs()
        if self.request.GET.get('group'):
            kwargs_dict.update({'initial': {'group': RoomGroup.objects.get(id=self.request.GET.get('group'))}})
            print(kwargs_dict)
        return kwargs_dict

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)