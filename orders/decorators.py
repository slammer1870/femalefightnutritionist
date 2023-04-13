from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from urllib3 import HTTPResponse

from .models import InitialCheckIn


def has_completed_checkin(view_func):
    @wraps(view_func)
    def inner(request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.order_set.filter(id=pk).exists():
                if InitialCheckIn.objects.filter(order=pk).exists():
                    return view_func(request, pk, *args, **kwargs)
                else:
                    return redirect('orders:initial-checkin', pk=pk)
            else:
                return redirect('users:dashboard')
        else:
            return redirect('users:login')
    return inner


def user_owns_order(view_func):
    @wraps(view_func)
    def inner(request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.order_set.filter(id=pk).exists():
                return view_func(request, pk, *args, **kwargs)
            else:
                return redirect('users:dashboard')
        else:
            return redirect('users:login')
    return inner
