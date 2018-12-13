from django import forms
from django.utils.timezone import now

from dps_main.utilities.actions import ActionHelper


class MakePromiseForm(forms.Form):
    cause_id = forms.IntegerField(widget=forms.HiddenInput())
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    current_url = forms.CharField(widget=forms.HiddenInput())
    amount = forms.FloatField(label='Promise Amount (NGN)', min_value=1.0, required=True, initial=1.0)
    target_date = forms.DateField(
        label='Target Date',
        required=True,
        initial=now().today(),
        widget=forms.DateInput(attrs={'type': 'date'}))

    def make_promise(self, helper: ActionHelper):
        helper.add_promise_to_cause(
            cause_id=self.cleaned_data['cause_id'],
            user_id=self.cleaned_data['user_id'],
            amount=self.cleaned_data['amount'],
            target_date=self.cleaned_data['target_date']
        )
