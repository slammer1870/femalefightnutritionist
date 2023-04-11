from django.contrib import admin

from .models import Journal, Order

# Register your models here.
admin.site.register(Order)
admin.site.register(Journal)
