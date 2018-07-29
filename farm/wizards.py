from django.shortcuts import HttpResponseRedirect, reverse
from django.forms import ModelForm
from django.forms.formsets import formset_factory

from easyfat_ui.views import EasyFatWizardView
from farm.views import FarmAccessMixin
from flocks.forms import FlockEntryForm

from .models import Farm, FarmFlockRelations

from .forms import FarmAnimalEntryRoomInformation


class NewAnimalEntryWizard(FarmAccessMixin, EasyFatWizardView):
    form_list = [('flock', FlockEntryForm),
                 ('room', formset_factory(form=FarmAnimalEntryRoomInformation, extra=10))]

    title_dict = {'flock': 'General Information'}

    def get_context_data(self, form, **kwargs):
        data = FarmAccessMixin.get_context_data(self, form, **kwargs)
        data.update(EasyFatWizardView.get_context_data(self, form, **kwargs))
        data.update({'bread_crumbs': [data['farm'].name, 'New Animal Entry']})
        return data

    def done(self, form_list, form_dict, **kwargs):
        flock_form = form_dict['flock']
        assert isinstance(flock_form, FlockEntryForm)
        flock = flock_form.save()
        flock.farmflockrelations_set.create(farm=Farm.objects.get(id=self.request.session['farm']))
        for form in form_dict['room']:
            assert isinstance(form, FarmAnimalEntryRoomInformation)
            if form.has_changed():
                entry = form.save(commit=False)
                entry.date = flock_form.cleaned_data['entry_date']
                entry.save()

        return HttpResponseRedirect(reverse('farm:index'))

