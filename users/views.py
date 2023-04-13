from datetime import datetime, timedelta

import simplejson as json
import stripe
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from djstripe import settings as djstripe_settings
from djstripe.models import Customer

from orders.models import InitialCheckIn, Order

from .forms import RegisterForm

stripe.api_key = djstripe_settings.djstripe_settings.STRIPE_SECRET_KEY

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

# Login Required.


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = 'dashboard.html'
    context_object_name = 'orders'

    def goal_weight(self, request):
        order = Order.objects.filter(user=request.user)

        # filter for order where comp date of before today

        if order.exists():

            initial_checkin = InitialCheckIn.objects.filter(
                order=order.first(), comp_date__gte=datetime.today())

            if initial_checkin.exists():

                initial_checkin = initial_checkin.last()

                start_date = initial_checkin.start_date
                comp_date = initial_checkin.comp_date

                starting_weight = float(initial_checkin.starting_weight)
                goal_weight = float(initial_checkin.goal_weight)

                date = start_date

                weight = starting_weight

                data_set = []

                labels = []

                labels.append(start_date.strftime(
                    "%y-%m-%d"))

                data_set.append(starting_weight)

                # calculate data as a percentage based loss of body weight
                while (weight > goal_weight and date <= comp_date):
                    date = date + timedelta(days=7)
                    weight = weight - \
                        (weight*float(0.01))
                    data_set.append(
                        weight)
                    labels.append(date.strftime("%y-%m-%d"))

                context = {
                    "labels": labels,
                    "data_set": json.dumps(data_set),
                    "starting_weight": starting_weight,
                    "goal_weight": goal_weight,
                    "start_date": start_date.strftime("%y-%m-%d"),
                    "comp_date": comp_date.strftime("%y-%m-%d"),
                }

                return context

        else:
            return None

    def get_actual_weight(self, request):
        order = Order.objects.filter(user=request.user)

        if order.exists():

            initial_checkin = InitialCheckIn.objects.filter(
                order=order.first(), comp_date__gte=datetime.today())

            if initial_checkin.exists() and order.first().checkin_set.exists():

                initial_checkin = initial_checkin.first()

                checkins = order.first().checkin_set.all()

                weight = [{'x': initial_checkin.start_date.strftime(
                    "%y-%m-%d"), 'y': initial_checkin.starting_weight}]

                for checkin in checkins:
                    if (checkin.current_weight):
                        weight.append(
                            {'x': checkin.date.strftime("%y-%m-%d"), 'y': int(checkin.current_weight)})
                return weight

        return None

    def get_nutrients(self, request):
        order = Order.objects.filter(user=request.user)

        if order.exists():

            initial_checkin = InitialCheckIn.objects.filter(
                order=order.first(), comp_date__gte=datetime.today())

            if initial_checkin.exists() and order.first().program_set.exists():

                program = order.first().program_set.filter(date=datetime.today())

                if program.exists():
                    program = program.first()

                    total_protein = program.protein
                    total_carbs = program.carbohydrate
                    total_fat = program.fat
                    total_calories = total_protein*4 + total_carbs*4 + total_fat*9

                    nutrients = {
                        'protein': total_protein,
                        'carbohydrate': total_carbs,
                        'fat': total_fat,
                        'calories': total_calories
                    }
                    return nutrients
        return None

    def get_context_data(self, **kwargs):
        goal_weight = self.goal_weight(self.request)
        checkin = self.get_actual_weight(self.request)
        program = self.get_nutrients(self.request)

        context = super().get_context_data(**kwargs)
        context['today'] = datetime.today()
        context['subscription'] = Customer(
            id=self.request.user.stripe_customer_id).has_any_active_subscription()

        if goal_weight:
            context['labels'] = goal_weight['labels']
            context['data_set'] = goal_weight['data_set']
            context['starting_weight'] = goal_weight['starting_weight']
            context['goal_weight'] = goal_weight['goal_weight']
            context['start_date'] = goal_weight['start_date']
            context['comp_date'] = goal_weight['comp_date']

        if checkin:
            context['checkin'] = True
            context['weight'] = json.dumps(checkin,  use_decimal=True)

        if program:
            context['program'] = True
            context['protein'] = program['protein']
            context['carbohydrate'] = program['carbohydrate']
            context['fat'] = program['fat']
            context['calories'] = program['calories']

        return context


@login_required
def create_customer_portal(request):

    session = stripe.billing_portal.Session.create(
        customer=request.user.stripe_customer_id,
        return_url=request.META['HTTP_REFERER'],
    )
    return redirect(session.url)
