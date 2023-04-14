# Generated by Django 3.2.14 on 2023-04-13 20:54

from django.db import migrations, models
import django_editorjs.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', django_editorjs.fields.EditorJsField()),
            ],
        ),
    ]
