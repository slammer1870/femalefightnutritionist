from datetime import datetime

from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic import FormView, ListView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from .forms import JournalForm
from .models import CheckIn, Journal, Order

# Create your views here.


class OrderListView(ListView):

    template_name = "orders/order_list.html"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class JournalListView(FormMixin, ListView):

    template_name = "orders/order_journal_list.html"
    form_class = JournalForm
    model = Journal

    def get_queryset(self, *args, **kwargs):
        if Journal.objects.filter(order__user=self.request.user, order_id=self.kwargs['pk'], date=datetime.today()).exists():
            return Journal.objects.filter(order__user=self.request.user, order_id=self.kwargs['pk'], date=datetime.today())
        else:
            return Journal.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = JournalForm()
        context['journal'] = True
        context['today'] = datetime.today()
        context['pk'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            f = form.save(commit=False)
            f.order_id = self.kwargs['pk']
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('orders:order-journal', kwargs={'pk': self.kwargs['pk']})


class CheckInListView(ListView):
    template_name = 'orders/order_checkin_list.html'

    model = CheckIn

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['checkin'] = True
        context['pk'] = self.kwargs['pk']
        return context

    def get_queryset(self, *args, **kwargs):
        if CheckIn.objects.filter(order__user=self.request.user, order_id=self.kwargs['pk']).exists():
            return CheckIn.objects.filter(order__user=self.request.user, order_id=self.kwargs['pk'])
        else:
            return CheckIn.objects.none()
