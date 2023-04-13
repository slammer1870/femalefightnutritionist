import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import ListView
from djstripe.models import Product

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductListView(ListView):
    queryset = Product.objects.filter(active=True)
    template_name = 'products/product_list.html'

    def post(self, request):
        customer_id = request.user.stripe_customer_id

        print('products is', request.POST.get('product'))

        # Gets the membership type from hidden input in form
        product = Product.objects.get(id=request.POST.get('product'))

        print(product.prices.first().type)

        if product.prices.first().type == "one_time":
            mode = "payment"
        else:
            mode = "subscription"

        try:
            checkout_session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': product.prices.first().id,
                        'quantity': 1,
                    },
                ],

                mode=mode,
                allow_promotion_codes=True,
                # Redirects to referer url
                success_url=request.build_absolute_uri() +
                'orders/success/{CHECKOUT_SESSION_ID}/',
                cancel_url=request.build_absolute_uri('/users/dashboard/')
            )
            return redirect(checkout_session.url, code=303)

        except Exception as e:
            print(e)
            return e
