from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from .views import ProductListView

app_name = "products"

urlpatterns = [
    path('', ProductListView.as_view(), name="product-list"),
]
