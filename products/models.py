from django.db import models

# Create your models here.

MODE_CHOICES = [('payment', 'payment'), ('subscription', 'subscription')]
FREQ_CHOICES = [('/month', '/month'), ('/week', '/week')]


class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    price = models.IntegerField()
    slug = models.SlugField()
    thumbnail = models.ImageField(upload_to='product_thumbnails', null=True)
    description = models.CharField(max_length=250)
    stripe_price_id = models.CharField(max_length=50)
    mode = models.CharField(max_length=250, choices=MODE_CHOICES)
    frequency = models.CharField(
        max_length=250, choices=FREQ_CHOICES, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)
