from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from .views import DashboardView, register

app_name = "users"

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('dashboard/', DashboardView.as_view(), name="dashboard")
]
