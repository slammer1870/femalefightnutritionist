from django.urls import path

from .decorators import has_completed_checkin
from .views import (CheckInFormView, CheckInListView, InitialCheckinView,
                    JournalListView, OrderListView, ProgramDateView,
                    ProgramView)

app_name = "orders"

urlpatterns = [
    path('', OrderListView.as_view(), name="order-list"),
    path('<pk>/initial-checkin/',
         InitialCheckinView.as_view(), name="initial-checkin"),
    path('<pk>/journal/', JournalListView.as_view(), name="journal-list"),
    path('<pk>/checkins/', CheckInListView.as_view(), name="checkin-list"),
    path('<pk>/checkins/<id>/', CheckInFormView.as_view(), name="checkin-form"),
    path('<pk>/programs/', ProgramView.as_view(), name="program-view"),
    path('<pk>/programs/<date>', ProgramDateView.as_view(), name="program-date"),

]
