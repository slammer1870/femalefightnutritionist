# Generated by Django 3.2.14 on 2023-04-11 13:45

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20230411_1339'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('medication', models.CharField(blank=True, max_length=400, verbose_name='Are you currently on any medications? if yes, please give details')),
                ('contraceptive', models.CharField(blank=True, max_length=400, verbose_name='Are you currently taking/using a contraceptive? If yes, please state which type')),
                ('goal_weight', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='Fight/goal weight (in kg)')),
                ('current_weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Current weight (in kg)')),
                ('height', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='Height (in cm)')),
                ('neck', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='Neck (in cm)')),
                ('waist', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='Waist (in cm)')),
                ('hip', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='Hip (in cm)')),
                ('left_bicep', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='Left bicep (in cm)')),
                ('left_quad', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, verbose_name='Left quad (in cm)')),
                ('energy', models.CharField(blank=True, choices=[('Very Low', 'Very Low'), ('Low', 'Low'), ('Average', 'Average'), ('High', 'High'), ('Very High', 'Very High')], max_length=400, verbose_name='How was your energy this week?')),
                ('stress', models.CharField(blank=True, choices=[('Not Stressed', 'Not Stressed'), ('Some Stress', 'Some Stress'), ('Average Stress', 'Average Stress'), ('Quite Stressed', 'Quite Stressed'), ('Very Stressed', 'Very Stressed')], max_length=400, verbose_name='How were your stress levels this week?')),
                ('sleep', models.CharField(blank=True, choices=[('Very Poor', 'Very Poor'), ('Below Average', 'Below Average'), ('Average', 'Average'), ('Good', 'Good'), ('Very Good', 'Very Good')], max_length=400, verbose_name='How was your sleep this week?')),
                ('hunger', models.CharField(blank=True, choices=[('No', 'No'), ('At times', 'At times'), ('A lot of the time', 'A lot of the time')], max_length=400, verbose_name='Were you hungry this week?')),
                ('percentage', models.CharField(blank=True, choices=[('10%', '10%'), ('20%', '20%'), ('30%', '30%'), ('40%', '40%'), ('50%', '50%'), ('60%', '60%'), ('70%', '70%'), ('80%', '80%'), ('90%', '90%'), ('100%', '100%')], max_length=400, verbose_name='As a percentage, how much did you adhere to your food plan this week?')),
                ('consume', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unsure', 'Unsure')], max_length=400, verbose_name='Did you over or under consume calories by more than 20 percent any day since last check in?')),
                ('consume_reasons', models.CharField(blank=True, choices=[('Hunger/Cravings', 'Hunger/Cravings'), ('Socialising', 'Socialising'), ('Not being prepared', 'Not being prepared'), ('Other', 'Other')], max_length=400, verbose_name='Over/Under Consumption: What was the main reason for this?')),
                ('period_date', models.DateField(blank=True, default=datetime.datetime(2023, 4, 11, 13, 45, 38, 148893, tzinfo=utc), verbose_name='When is your next period due?')),
                ('digestive_issues', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Unsure', 'Unsure')], max_length=400, verbose_name='Have you had any digestive issues this week?i.e. gas, bloating, diarrhoea, etc.')),
                ('digestive_describe', models.CharField(blank=True, max_length=400, verbose_name='Describe your digestive issues  or write "n/a" if you did not have any')),
                ('bowel_frequency', models.CharField(blank=True, choices=[('Multiple times per day', 'Multiple times per day'), ('Once a day', 'Once a day'), ('Every other day', 'Every other day'), ('Infrequent', 'Infrequent')], max_length=400, verbose_name='How frequent were your bowl movements this week?')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
        ),
    ]