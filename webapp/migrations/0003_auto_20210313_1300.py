# Generated by Django 3.1 on 2021-03-13 07:30

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='country',
            field=django_countries.fields.CountryField(default='India', max_length=2),
        ),
    ]
