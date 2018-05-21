from formtools.wizard.views import SessionWizardView

from django.utils.translation import ugettext as _
from django.views.generic import FormView


class EasyFatWizardView(SessionWizardView):
    """This is a base class for the wizards inside EasyFat."""

    wizard_name = _('EasyFat Wizard')
    template_name = 'form_wizard.html'
    title_dict = {}

    def done(self, form_list, **kwargs):
        raise NotImplementedError('EasyFatWizard is only an abstraction.')

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context.update({'wizard_title': self.wizard_name})

        current_step = self.steps.current
        title = self.title_dict.get(current_step, current_step)
        context.update({'step_title': title})
        return context


class EasyFatFormView(FormView):
    template_name = 'single_form.html'
