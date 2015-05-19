# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forecast_type', models.CharField(max_length=2, choices=[(b'1', b'Binary'), (b'2', b'Probability'), (b'3', b'Magnitude'), (b'4', b'Temporal')])),
                ('forecast_question', models.TextField(max_length=1000)),
                ('start_date', models.DateField(auto_now=True)),
                ('end_date', models.DateField()),
            ],
            options={
                'ordering': ['-end_date'],
                'db_table': 'forecasts',
                'get_latest_by': 'start_date',
            },
        ),
        migrations.CreateModel(
            name='ForecastVotes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.IntegerField()),
                ('forecast_id', models.ForeignKey(to='app.Forecast')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organization_type', models.CharField(max_length=2, choices=[(b'1', b'School'), (b'2', b'Think Tank'), (b'3', b'Company'), (b'4', b'Government Agency')])),
                ('organization_name', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_only_username', models.BooleanField(default=False)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('profession', models.CharField(max_length=100, blank=True)),
                ('position', models.CharField(max_length=100, blank=True)),
                ('forecast_areas', models.CommaSeparatedIntegerField(max_length=3, blank=True)),
                ('forecast_regions', models.CommaSeparatedIntegerField(max_length=3, blank=True)),
                ('activation_token', models.TextField(blank=True)),
                ('expires_at', models.DateTimeField(blank=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(to='app.Organization')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='forecastvotes',
            name='user_id',
            field=models.ForeignKey(to='app.UserProfile'),
        ),
    ]
