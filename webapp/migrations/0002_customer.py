# Generated by Django 3.1 on 2021-03-12 12:31

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=80)),
                ('lastname', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=12)),
                ('website', models.URLField(max_length=1000)),
                ('position', models.CharField(max_length=200)),
                ('company', models.CharField(max_length=100)),
                ('gst_number', models.CharField(max_length=200)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('city', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
    ]