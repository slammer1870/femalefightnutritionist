from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email']


class NewsletterForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
