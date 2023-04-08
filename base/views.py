from django.contrib import messages
from django.shortcuts import render
from django.views import generic

from .forms import LeadForm


class IndexPageView(generic.FormView):
    template_name = "index.html"
    form_class = LeadForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, "Thank you, we will be in touch shortly")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "It seems you have registered already")
        return super().form_invalid(form)
        