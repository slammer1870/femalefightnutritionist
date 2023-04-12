"""
URL configuration for femalefightnutritionist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import include, path

from base.views import IndexPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', IndexPageView.as_view(), name="index"),
    path('password-reset/', PasswordResetView.as_view(), name="password_reset"),
    path('password-reset-done/', PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    path('users/', include('users.urls', namespace='users')),
    path('products/', include('products.urls', namespace='products')),
    path('orders/', include('orders.urls', namespace='orders')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    path("stripe/", include("djstripe.urls", namespace="djstripe")),

]
