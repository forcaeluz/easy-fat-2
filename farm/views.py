from django.views.generic import TemplateView, View
from django.urls.base import reverse_lazy
from django.shortcuts import HttpResponseRedirect, reverse
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.core.exceptions import PermissionDenied

from easyfat_ui.views import EasyFatFormView
from .forms import NewFarmForm
from .models import Farm


class FarmAccessMixin(AccessMixin):

    @staticmethod
    def test_for_farm_access(user, farm_id):
        if Farm.objects.filter(id=farm_id):
            farm = Farm.objects.get(id=farm_id)
            result = farm.userfarmrelations_set.filter(user=user)
            return result.count() > 0

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        elif kwargs.get('farm_id'):
            if self.test_for_farm_access(request.user, kwargs.get('farm_id')):
                request.session['farm'] = kwargs.get('farm_id')
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied('You have no access to selected farm.')

        elif request.user.userfarmrelations_set.count() == 0:
            request.session['farm'] = None
            return HttpResponseRedirect(reverse('accounts:index'))

        elif request.session.get('farm') and self.test_for_farm_access(request.user, request.session.get('farm')):
            return super().dispatch(request, *args, **kwargs)

        else:
            request.session['farm'] = request.user.userfarmrelations_set.all()[0].farm.id
            return super().dispatch(request, *args, **kwargs)


class FarmIndexView(FarmAccessMixin, TemplateView):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        farm = Farm.objects.get(id=self.request.session['farm'])
        data.update({'farm': farm})
        kpi_info = {'color': 'primary',
                    'icon': 'bug',
                    'value': '512',
                    'description': 'Animals in the farm',
                    'action': '#',
                    'action_name': 'View Details'}
        data.update({'kpi_info': kpi_info})
        data.update({'bread_crumbs': [farm.name, 'Dashboard']})

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

