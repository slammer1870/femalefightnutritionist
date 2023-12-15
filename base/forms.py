from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email']


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    message = forms.CharField(label='Message', max_length=250, widget=forms.Textarea(
        attrs={'rows': 5, 'cols': 10}))
