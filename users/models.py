import stripe
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djstripe import settings as djstripe_settings

# Create your views here.

stripe.api_key = djstripe_settings.djstripe_settings.STRIPE_SECRET_KEY


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    stripe_customer_id = models.CharField(max_length=50, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# Receiver to create customer in Stripe and assing their StripeID to the CustomUser object


@receiver(post_save, sender=CustomUser)
def create_stripe_id(sender, instance, **kwargs):

    name = str("{0} {1}").format(instance.first_name, instance.last_name)

    if instance.stripe_customer_id == None:

        stripe_customer = stripe.Customer.create(
            name=name,
            email=instance.email
        )

        instance.stripe_customer_id = stripe_customer["id"]

        post_save.disconnect(create_stripe_id, sender=CustomUser)
        instance.save()
        post_save.connect(create_stripe_id, sender=CustomUser)
