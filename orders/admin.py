from django.contrib import admin

from .models import CheckIn, InitialCheckIn, Journal, Order, Program

# Register your models here.
admin.site.register(Order)
admin.site.register(Journal)
admin.site.register(CheckIn)
admin.site.register(Program)
admin.site.register(InitialCheckIn)
