# Generated by Django 3.2.14 on 2023-04-14 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20230414_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='quillpost',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]