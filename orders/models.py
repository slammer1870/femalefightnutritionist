from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
        ordering = ('-purchase_date',)  # Sort in desc order

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

    @property
    def total_calories(self):
        if self.protein and self.carbohydrate and self.fat:
            return (self.protein*4 + self.carbohydrate*4 + self.fat*9)
        else:
            return None

    def __str__(self):
        return "{0} - {1}".format(self.name, str(self.date))


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
        verbose_name='When is your next period due?', blank=True, default=timezone.now)
    digestive_issues = models.CharField(verbose_name='Have you had any digestive issues this week?i.e. gas, bloating, diarrhoea, etc.',
                                        max_length=400, choices=DIGESTIVE_CHOICES, blank=True)
    digestive_describe = models.CharField(
        verbose_name='Describe your digestive issues  or write "n/a" if you did not have any', max_length=400, blank=True)
    bowel_frequency = models.CharField(verbose_name='How frequent were your bowl movements this week?',
                                       max_length=400, choices=BOWEL_CHOICES, blank=True)

    def __str__(self):
        return "Check In - {0}".format(str(self.date))

    class Meta:
        ordering = ('date',)


@receiver(post_save, sender=CheckIn)
def send_checkin_email(sender, instance, created, **kwargs):
    if not created:
        subject = f'New Check-In Form submitted on {instance.date} by {instance.order.user}.'
        message = f'New Check-In Form submitted on {instance.date} by {instance.order.user}. Details:\n\n'
        message += f'Order: {instance.order}\n\n'
        message += f'Medication: {instance.medication}\n\n'
        message += f'Contraceptive: {instance.contraceptive}\n\n'
        message += f'Goal Weight: {instance.goal_weight}\n\n'
        message += f'Current Weight: {instance.current_weight}\n\n'
        message += f'Height: {instance.height}\n\n'
        message += f'Neck: {instance.neck}\n\n'
        message += f'Waist: {instance.waist}\n\n'
        message += f'Hip: {instance.hip}\n\n'
        message += f'Left Bicep: {instance.left_bicep}\n\n'
        message += f'Left Quad: {instance.left_quad}\n\n'
        message += f'Energy: {instance.energy}\n\n'
        message += f'Stress: {instance.stress}\n\n'
        message += f'Sleep: {instance.sleep}\n\n'
        message += f'Hunger: {instance.hunger}\n\n'
        message += f'Percentage: {instance.percentage}\n\n'
        message += f'Consume: {instance.consume}\n\n'
        message += f'Consume Reasons: {instance.consume_reasons}\n\n'
        message += f'Period Date: {instance.period_date}\n\n'
        message += f'Digestive Issues: {instance.digestive_issues}\n\n'
        message += f'Digestive Describe: {instance.digestive_describe}\n\n'
        message += f'Bowel Frequency: {instance.bowel_frequency}\n\n'
        # Replace with desired recipient email address
        recipient_list = [settings.DEFAULT_FROM_EMAIL]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


class Program(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateField()
    protein = models.IntegerField()
    carbohydrate = models.IntegerField()
    fat = models.IntegerField()
    hydration = models.IntegerField()
    suplements = models.CharField(max_length=400)

    def __str__(self):
        return "Program - {0}".format(str(self.date))


class InitialCheckIn(models.Model):
    order = models.OneToOneField(
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
    medication = models.CharField(
        verbose_name='Are you currently on any medications? if yes, please give details', max_length=400)
    contraceptive = models.CharField(
        verbose_name='Are you currently taking/using a contraceptive? If yes, please state which type', max_length=400)
    height = models.DecimalField(
        verbose_name='Height (in cm)', default=0, max_digits=5, decimal_places=2)
    neck = models.DecimalField(
        verbose_name='Neck (in cm)', default=0, max_digits=5, decimal_places=2)
    waist = models.DecimalField(
        verbose_name='Waist (in cm)', default=0, max_digits=5, decimal_places=2)
    hip = models.DecimalField(
        verbose_name='Hip (in cm)', default=0, max_digits=5, decimal_places=2)
    left_bicep = models.DecimalField(
        verbose_name='Left bicep (in cm)', default=0, max_digits=5, decimal_places=2)
    left_quad = models.DecimalField(
        verbose_name='Left quad (in cm)', default=0, max_digits=5, decimal_places=2)
    energy = models.CharField(verbose_name='How was your energy this week?',
                              max_length=400, choices=ENERGY_CHOICES)
    stress = models.CharField(verbose_name='How were your stress levels this week?',
                              max_length=400, choices=STRESS_CHOICES)
    sleep = models.CharField(verbose_name='How was your sleep this week?',
                             max_length=400, choices=SLEEP_CHOICES)
    period_date = models.DateField(
        verbose_name='When is your next period due?', default=timezone.now)
    digestive_issues = models.CharField(verbose_name='Have you had any digestive issues this week?i.e. gas, bloating, diarrhoea, etc.',
                                        max_length=400, choices=DIGESTIVE_CHOICES)
    digestive_describe = models.CharField(
        verbose_name='Describe your digestive issues  or write "n/a" if you did not have any', max_length=400)
    bowel_frequency = models.CharField(verbose_name='How frequent were your bowl movements this week?',
                                       max_length=400, choices=BOWEL_CHOICES)
    extra = models.CharField(verbose_name='Anything more you would like to briefly comment on or share about yourself?',
                             max_length=400)

    def __str__(self):
        return str(self.order)


@receiver(post_save, sender=InitialCheckIn)
def send_initial_checkin_email(sender, instance, created, **kwargs):
    subject = f'New Initial Check-In Form submitted on {instance.checkin_time} by {instance.order.user}.'
    message = f'New Initial Check-In Form submitted on {instance.checkin_time} by {instance.order.user}. Details:\n\n'
    message += f'Order: {instance.order}\n\n'
    message += f'Medication: {instance.medication}\n\n'
    message += f'Contraceptive: {instance.contraceptive}\n\n'
    message += f'Goal Weight: {instance.goal_weight}\n\n'
    message += f'Current Weight: {instance.starting_weight}\n\n'
    message += f'Height: {instance.height}\n\n'
    message += f'Neck: {instance.neck}\n\n'
    message += f'Waist: {instance.waist}\n\n'
    message += f'Hip: {instance.hip}\n\n'
    message += f'Left Bicep: {instance.left_bicep}\n\n'
    message += f'Left Quad: {instance.left_quad}\n\n'
    message += f'Energy: {instance.energy}\n\n'
    message += f'Stress: {instance.stress}\n\n'
    message += f'Sleep: {instance.sleep}\n\n'
    message += f'Period Date: {instance.period_date}\n\n'
    message += f'Digestive Issues: {instance.digestive_issues}\n\n'
    message += f'Digestive Describe: {instance.digestive_describe}\n\n'
    message += f'Bowel Frequency: {instance.bowel_frequency}\n\n'
    # Replace with desired recipient email address
    recipient_list = [settings.DEFAULT_FROM_EMAIL]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
