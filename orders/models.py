from django.conf import settings
from django.db import models
from django.utils import timezone

from products.models import Product

# Create your models here.


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    stripe_purchase_id = models.CharField(max_length=250)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "User: {0}, Order: {1}".format(self.user.first_name, str(self.id))


class Journal(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=180, null=True)
    protein = models.IntegerField(default=0)
    carbohydrate = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    hydration = models.IntegerField(
        verbose_name="Hydration (in litres)", blank=True, null=True)
    suplements = models.CharField(max_length=400, null=True, blank=True)
