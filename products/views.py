from django.shortcuts import render
from django.views.generic import ListView

from .models import Product

# Create your views here.


class ProductListView(ListView):
    queryset = Product.objects.filter(active=True)
    template_name = 'products/product_list.html'
