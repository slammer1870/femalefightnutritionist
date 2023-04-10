
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .forms import RegisterForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

#Login Required
class DashboardView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "dashboard.html")
