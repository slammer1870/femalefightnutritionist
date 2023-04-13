from datetime import datetime

from django import forms
from django.forms import ModelForm

from .models import CheckIn, InitialCheckIn, Journal


class JournalForm(ModelForm):
    class Meta:
        model = Journal
        exclude = ['order', 'date']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. "Breakfast"'})
        }

    def __init__(self, *args, **kwargs):
        super(JournalForm, self).__init__(*args, **kwargs)
        self.fields['suplements'].required = False
        self.fields['hydration'].required = False


class CheckInForm(ModelForm):
    class Meta:
        model = CheckIn
        exclude = ['order', 'date']

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date


class InitialCheckInForm(ModelForm):

    comp_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    def clean_date(self):
        date = self.cleaned_data['comp_date']
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date

    class Meta:
        model = InitialCheckIn
        exclude = ['order', ]
