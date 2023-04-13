from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline

from orders.models import CheckIn, InitialCheckIn, Journal, Order, Program

from .models import CustomUser


class OrderInline(admin.StackedInline):
    model = Order
    extra = 0


class InitialCheckInNestedInline(NestedStackedInline):
    model = InitialCheckIn
    extra = 0
    classes = ['collapse']


class JournalNestedInline(NestedStackedInline):
    model = Journal
    extra = 0
    readonly_fields = ('date', 'total_calories')
    classes = ['collapse']


class CheckInNestedInline(NestedStackedInline):
    model = CheckIn
    extra = 0
    ordering = ('-date',)
    classes = ['collapse']


class ProgramNestedInline(NestedStackedInline):
    model = Program
    extra = 0
    ordering = ('-date',)
    classes = ['collapse']


class OrderNestedInline(NestedStackedInline):
    model = Order
    fields = ['product', 'stripe_purchase_id',]
    readonly_fields = ['purchase_date']
    ordering = ['purchase_date']
    extra = 0
    inlines = [InitialCheckInNestedInline, JournalNestedInline,
               CheckInNestedInline, ProgramNestedInline]


class UserNestedAdmin(NestedModelAdmin):
    exclude = ('is_staff', 'is_superuser', 'is_active', 'groups')
    inlines = [OrderNestedInline]


class CustomUserAdmin(NestedModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    exclude = ('is_staff', 'is_superuser', 'is_active',
               'groups', 'user_permissions', 'password')
    readonly_fields = ('email', 'first_name', 'last_name',
                       'stripe_customer_id', 'date_joined', 'last_login')

    inlines = [OrderNestedInline]


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'purshase_date')
    search_fields = ('user',)
    ordering = ('-purchase_date')


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(InitialCheckIn)
