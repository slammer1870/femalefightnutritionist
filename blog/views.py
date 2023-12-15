from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Post

# Create your views here.


class BlogListView(ListView):
    template_name = "blog/blog_list.html"
    model = Post
    queryset = Post.objects.filter(published=True)


class BlogDetailView(DetailView):
    template_name = "blog/blog_detail.html"
    model = Post
    queryset = Post.objects.filter(published=True)
