# Generated by Django 3.2.14 on 2023-04-13 09:13

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20230412_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='period_date',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 4, 13, 9, 13, 39, 633266, tzinfo=utc), verbose_name='When is your next period due?'),
        ),
        migrations.AlterField(
            model_name='initialcheckin',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='initial_checkin', to='orders.order'),
        ),
    ]