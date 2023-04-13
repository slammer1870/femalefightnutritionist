from django.conf import settings
from django.db import models
from django.utils import timezone
from djstripe.models import Product

# Create your models here.


class Order(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, db_constraint=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    stripe_purchase_id = models.CharField(max_length=250)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-purchase_date']  # Sort in desc order

    def __str__(self):
        return "User: {0}, Order: {1}".format(self.user.first_name, str(self.id))


class Journal(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=180, null=True)
    protein = models.IntegerField()
    carbohydrate = models.IntegerField()
    fat = models.IntegerField()
    hydration = models.IntegerField(
        verbose_name="Hydration (in litres)", blank=True, null=True)
    suplements = models.CharField(max_length=400, null=True, blank=True)


ENERGY_CHOICES = [('Very Low', 'Very Low'), ('Low', 'Low'),
                  ('Average', 'Average'), ('High', 'High'), ('Very High', 'Very High')]
STRESS_CHOICES = [('Not Stressed', 'Not Stressed'), ('Some Stress', 'Some Stress'),
                  ('Average Stress', 'Average Stress'), ('Quite Stressed', 'Quite Stressed'), ('Very Stressed', 'Very Stressed')]
SLEEP_CHOICES = [('Very Poor', 'Very Poor'), ('Below Average', 'Below Average'),
                 ('Average', 'Average'), ('Good', 'Good'), ('Very Good', 'Very Good')]
HUNGER_CHOICES = [('No', 'No'), ('At times', 'At times'),
                  ('A lot of the time', 'A lot of the time')]
PERCENT_COICES = [('10%', '10%'), ('20%', '20%'), ('30%', '30%'), ('40%', '40%'), ('50%', '50%'),
                  ('60%', '60%'), ('70%', '70%'), ('80%', '80%'), ('90%', '90%'), ('100%', '100%')]
CONSUME_CHOICES = [('Yes', 'Yes'), ('No', 'No'), ('Unsure', 'Unsure')]
CONSUME_REASONS = [('Hunger/Cravings', 'Hunger/Cravings'), ('Socialising', 'Socialising'),
                   ('Not being prepared', 'Not being prepared'), ('Other', 'Other')]
DIGESTIVE_CHOICES = [('Yes', 'Yes'), ('No', 'No'), ('Unsure', 'Unsure')]
BOWEL_CHOICES = [('Multiple times per day', 'Multiple times per day'), ('Once a day', 'Once a day'),
                 ('Every other day', 'Every other day'), ('Infrequent', 'Infrequent')]


class CheckIn(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateField()
    medication = models.CharField(
        verbose_name='Are you currently on any medications? if yes, please give details', max_length=400, blank=True)
    contraceptive = models.CharField(
        verbose_name='Are you currently taking/using a contraceptive? If yes, please state which type', max_length=400, blank=True)
    goal_weight = models.DecimalField(
        verbose_name='Fight/goal weight (in kg)', blank=True, default=0, max_digits=5, decimal_places=2)
    current_weight = models.DecimalField(
        verbose_name='Current weight (in kg)', blank=True, null=True, max_digits=5, decimal_places=2)
    height = models.DecimalField(
        verbose_name='Height (in cm)', blank=True, default=0, max_digits=5, decimal_places=2)
    neck = models.DecimalField(
        verbose_name='Neck (in cm)', blank=True, default=0, max_digits=5, decimal_places=2)
    waist = models.DecimalField(
        verbose_name='Waist (in cm)', blank=True, default=0, max_digits=5, decimal_places=2)
    hip = models.DecimalField(
        verbose_name='Hip (in cm)', blank=True, default=0, max_digits=5, decimal_places=2)
    left_bicep = models.DecimalField(
        verbose_name='Left bicep (in cm)', blank=True, default=0, max_digits=5, decimal_places=2)
    left_quad = models.DecimalField(
        verbose_name='Left quad (in cm)', blank=True, default=0, max_digits=5, decimal_places=2)
    energy = models.CharField(verbose_name='How was your energy this week?',
                              max_length=400, choices=ENERGY_CHOICES, blank=True)
    stress = models.CharField(verbose_name='How were your stress levels this week?',
                              max_length=400, choices=STRESS_CHOICES, blank=True)
    sleep = models.CharField(verbose_name='How was your sleep this week?',
                             max_length=400, choices=SLEEP_CHOICES, blank=True)
    hunger = models.CharField(verbose_name='Were you hungry this week?',
                              max_length=400, choices=HUNGER_CHOICES, blank=True)
    percentage = models.CharField(verbose_name='As a percentage, how much did you adhere to your food plan this week?',
                                  max_length=400, choices=PERCENT_COICES, blank=True)
    consume = models.CharField(verbose_name='Did you over or under consume calories by more than 20 percent any day since last check in?',
                               max_length=400, choices=CONSUME_CHOICES, blank=True)
    consume_reasons = models.CharField(verbose_name='Over/Under Consumption: What was the main reason for this?',
                                       max_length=400, choices=CONSUME_REASONS, blank=True)
    period_date = models.DateField(
        verbose_name='When is your next period due?', blank=True, default=timezone.now())
    digestive_issues = models.CharField(verbose_name='Have you had any digestive issues this week?i.e. gas, bloating, diarrhoea, etc.',
                                        max_length=400, choices=DIGESTIVE_CHOICES, blank=True)
    digestive_describe = models.CharField(
        verbose_name='Describe your digestive issues  or write "n/a" if you did not have any', max_length=400, blank=True)
    bowel_frequency = models.CharField(verbose_name='How frequent were your bowl movements this week?',
                                       max_length=400, choices=BOWEL_CHOICES, blank=True)


class Program(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateField()
    protein = models.IntegerField()
    carbohydrate = models.IntegerField()
    fat = models.IntegerField()
    hydration = models.IntegerField()
    suplements = models.CharField(max_length=400)


class InitialCheckIn(models.Model):
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='initial_checkin'
    )
    checkin_time = models.DateTimeField(auto_now_add=True)

    starting_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    goal_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    start_date = models.DateField(
        auto_now_add=True
    )
    comp_date = models.DateField(verbose_name="Competition Date (YYYY-MM-DD)")

    def __str__(self):
        return str(self.order)
