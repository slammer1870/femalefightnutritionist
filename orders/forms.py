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


class InitialCheckInForm(ModelForm):
    class Meta:
        model = InitialCheckIn
        exclude = ['order', ]
