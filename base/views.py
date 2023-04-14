from django.contrib import messages
from django.shortcuts import render
from django.views import generic

from blog.models import Post

from .forms import LeadForm


class IndexPageView(generic.FormView):
    template_name = "index.html"
    form_class = LeadForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_posts'] = Post.objects.all()[:3]

        return context

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, "Thank you, we will be in touch shortly")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "It seems you have registered already")
        return super().form_invalid(form)
