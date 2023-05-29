from datetime import datetime, timedelta

import stripe
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView, TemplateView, UpdateView
from django.views.generic.edit import FormMixin
from djstripe import settings as djstripe_settings
from djstripe import webhooks
from djstripe.models import Price

from users.models import CustomUser

from .decorators import has_completed_checkin, user_owns_order
from .forms import CheckInForm, InitialCheckInForm, JournalForm
from .models import CheckIn, Journal, Order, Program

stripe.api_key = djstripe_settings.djstripe_settings.STRIPE_SECRET_KEY

# Create your views here.


@webhooks.handler('checkout.session.completed', 'customer.subscription.updated')
def create_new_order(event, **kwargs):

    # Retireve Event
    stripe_event = stripe.Event.retrieve(event.id)

    user_set = CustomUser.objects.filter(
        stripe_customer_id=stripe_event.data.object.customer)

    # Check Event Type

    if (user_set.exists()):

        user = user_set.first()

        # If event is a checkout session:
        if (event.type == 'checkout.session.completed'):
            line_items = stripe.checkout.Session.list_line_items(
                stripe_event.data.object.id, limit=5)

            price = line_items.data[0].price.id

            stripe_price = Price.objects.get(id=price)

            product = stripe_price.product

            order = Order.objects.create(user=user, product=product,
                                         stripe_purchase_id=stripe_event.data.object.payment_intent or stripe_event.data.object.subscription)

            return

        if (event.type == 'customer.subscription.updated'):

            price = stripe_event.data.object.items.data[0].price.id

            stripe_price = Price.objects.get(id=price)

            product = stripe_price.product

            order, created = Order.objects.get_or_create(
                user=user, product=product, stripe_purchase_id=stripe_event.data.object.id)

            return

        return

    return


class OrderListView(ListView):

    template_name = "orders/order_list.html"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


@ method_decorator(user_owns_order, name="dispatch")
class InitialCheckinView(FormView):
    template_name = "orders/initial_checkin.html"
    form_class = InitialCheckInForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('orders:journal-list', kwargs={'pk': self.kwargs['pk']})


@ method_decorator(has_completed_checkin, name="dispatch")
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
        return reverse('orders:journal-list', kwargs={'pk': self.kwargs['pk']})


@ method_decorator(has_completed_checkin, name="dispatch")
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


@ method_decorator(has_completed_checkin, name="dispatch")
class CheckInFormView(UpdateView):

    template_name = 'orders/order_checkin_form.html'
    form_class = CheckInForm

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(CheckIn, id=id_)

    def get_success_url(self, **kwargs):
        print()
        return reverse('orders:checkin-list', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['checkin'] = True
        context['pk'] = self.kwargs['pk']
        return context


@ method_decorator(has_completed_checkin, name="dispatch")
class ProgramView(TemplateView):

    template_name = 'orders/order_program.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['program'] = True
        context['pk'] = self.kwargs['pk']
        context['today'] = datetime.strftime(datetime.today(), "%Y-%m-%d")
        return context


@ method_decorator(has_completed_checkin, name="dispatch")
class ProgramDateView(TemplateView):

    template_name = 'orders/order_program_date.html'

    def get_context_data(self, **kwargs):
        try:
            program = Program.objects.get(
                order=self.kwargs['pk'], date=self.kwargs['date'])
        except Program.DoesNotExist:
            program = None

        context = super().get_context_data(**kwargs)
        context['program'] = program
        context['today'] = datetime.strptime(self.kwargs['date'], "%Y-%m-%d")
        context['tomorrow'] = datetime.strftime(datetime.strptime(
            self.kwargs['date'], "%Y-%m-%d") + timedelta(days=+1), "%Y-%m-%d")
        context['yesterday'] = datetime.strftime(datetime.strptime(
            self.kwargs['date'], "%Y-%m-%d") + timedelta(days=-1), "%Y-%m-%d") if datetime.strptime(
                self.kwargs['date'], "%Y-%m-%d") > datetime.today() else None

        context['pk'] = self.kwargs['pk']
        return context
