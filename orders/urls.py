from django.urls import path

from .views import JournalListView, OrderListView

app_name = "orders"

urlpatterns = [
    path('', OrderListView.as_view(), name="order-list"),
    path('<pk>/journal/', JournalListView.as_view(), name="order-journal"),
]
