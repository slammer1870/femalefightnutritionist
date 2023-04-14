# Generated by Django 3.2.14 on 2023-04-14 09:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_alter_checkin_period_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='period_date',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 4, 14, 9, 31, 51, 126526, tzinfo=utc), verbose_name='When is your next period due?'),
        ),
    ]
