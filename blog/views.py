from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import QuillPost

# Create your views here.


class BlogListView(ListView):
    template_name = "blog/blog_list.html"
    model = QuillPost


class BlogDetailView(DetailView):
    template_name = "blog/blog_detail.html"
    model = QuillPost
