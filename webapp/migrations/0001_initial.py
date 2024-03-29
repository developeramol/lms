# Generated by Django 3.1 on 2021-03-11 10:27

import colorful.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='lead_sources',
            fields=[
                ('source_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('total_lead', models.IntegerField(default=0)),
                ('user', models.CharField(default='SUPERADMIN', max_length=50)),
                ('status', models.CharField(choices=[('1', 'active'), ('2', 'inactive')], default='1', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='lead_status',
            fields=[
                ('status_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('background_color', colorful.fields.RGBColorField(colors=['#FF0000', '#00FF00', '#0000FF'])),
                ('text_color', colorful.fields.RGBColorField(colors=['#FF0000', '#00FF00', '#0000FF'])),
                ('total_lead', models.IntegerField(default=0)),
                ('user', models.CharField(default='SUPERADMIN', max_length=50)),
                ('status', models.CharField(choices=[('1', 'active'), ('2', 'inactive')], default='1', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_admin',
            fields=[
                ('admin_id', models.AutoField(primary_key=True, serialize=False)),
                ('mobile', models.CharField(max_length=10)),
                ('image', models.ImageField(blank=True, default='image/admin.png', upload_to='Admin_images/%Y/%m/%d/')),
                ('status', models.CharField(choices=[('1', 'active'), ('2', 'inactive')], default='1', max_length=20)),
                ('parent', models.CharField(default='SUPERADMIN', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_type', models.CharField(default='ADMIN', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='user_client',
            fields=[
                ('client_id', models.AutoField(primary_key=True, serialize=False)),
                ('mobile', models.CharField(max_length=10)),
                ('image', models.ImageField(blank=True, default='image/admin.png', upload_to='Admin_images/%Y/%m/%d/')),
                ('status', models.CharField(choices=[('1', 'active'), ('2', 'inactive')], default='1', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_type', models.CharField(default='CLIENT', max_length=10)),
                ('parent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='webapp.user_admin')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Historicalcreate_lead',
            fields=[
                ('lead_id', models.IntegerField(blank=True, db_index=True)),
                ('name', models.CharField(db_index=True, max_length=50)),
                ('query', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=10)),
                ('email', models.EmailField(db_index=True, max_length=50)),
                ('description', models.TextField(max_length=200)),
                ('remark', models.TextField(default='Created Lead')),
                ('follow_up_date', models.DateTimeField(null=True)),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('lead_assign', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='webapp.user_admin')),
                ('lead_sour', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='webapp.lead_sources')),
                ('lead_stat', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='webapp.lead_status')),
            ],
            options={
                'verbose_name': 'historical create_lead',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='create_lead',
            fields=[
                ('lead_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('query', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('description', models.TextField(max_length=200)),
                ('remark', models.TextField(default='Created Lead')),
                ('follow_up_date', models.DateTimeField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('lead_assign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.user_admin')),
                ('lead_sour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.lead_sources')),
                ('lead_stat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.lead_status')),
            ],
            options={
                'ordering': ['-lead_id'],
            },
        ),
    ]
