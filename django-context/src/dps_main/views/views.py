from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.views.generic import CreateView, ListView, DetailView, FormView

from dps_main.utilities.actions import ActionHelper
from ..forms import MakePromiseForm


class RegisterView(CreateView):
    """
    User registration
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class ActionPropertyMixin(object):
    """
    Mixin requires the following defined on the instance:
    - request
    """

    @property
    def action_helper(self) -> ActionHelper:
        """
        The user's action helper
        :return: ActionHelper
        """
        return self.request.action_helper


class AvailableCausesMixin(ActionPropertyMixin):
    """
    Mixin enables to work with available clauses
    """

    def get_queryset(self):
        return self.action_helper.list_available_causes()


class CausesListView(AvailableCausesMixin, ListView):
    """
    Show a list of causes
    """
    paginate_by = 15


class CausesPromiseDetailsView(AvailableCausesMixin, DetailView):
    """
    Show the detail of a `cause` and prepare it to accept a promise
    """

    def get_context_data(self, **kwargs):
        context = super(CausesPromiseDetailsView, self).get_context_data(**kwargs)
        form = MakePromiseForm()
        form.initial = {
            'user_id': self.request.user.pk,
            'cause_id': self.kwargs.get('pk'),
            'current_url': self.request.path
        }
        context['form'] = form
        return context


class MakePromiseFormView(ActionPropertyMixin, FormView):
    """
    Act's on promise post data
    """
    form_class = MakePromiseForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.make_promise(self.action_helper)
        self.success_url = form.cleaned_data.get('current_url', self.success_url)
        return super().form_valid(form)
