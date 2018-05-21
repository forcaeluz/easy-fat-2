from django.views.generic import TemplateView
from django.urls.base import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from easyfat_ui.views import EasyFatFormView
from .forms import NewFarmForm


class FarmIndexView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        kpi_info = {'color': 'primary',
                    'icon': 'bug',
                    'value': '512',
                    'description': 'Animals in the farm',
                    'action': '#',
                    'action_name': 'View Details'}
        data.update({'kpi_info': kpi_info})
        data.update({'bread_crumbs': ['Dashboard']})

        return data

    template_name = "farm/index.html"


class NewFarmView(LoginRequiredMixin, EasyFatFormView):
    form_class = NewFarmForm
    success_url = reverse_lazy('farm:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({'bread_crumbs': ['Forms', 'New Farm']})
        return data

    def form_valid(self, form):
        farm = form.save()
        user = self.request.user  # User
        relation = user.userfarmrelations_set.create(farm=farm, relation='owner')
        relation.save()
        return super().form_valid(form)
