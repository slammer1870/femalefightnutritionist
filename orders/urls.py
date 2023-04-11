from django.urls import path

from .views import CheckInListView, JournalListView, OrderListView

app_name = "orders"

urlpatterns = [
    path('', OrderListView.as_view(), name="order-list"),
    path('<pk>/journal/', JournalListView.as_view(), name="order-journal"),
    path('<pk>/checkins/', CheckInListView.as_view(), name="checkin-list"),
]
