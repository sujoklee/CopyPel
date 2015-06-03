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
            name='CustomUserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_only_username', models.BooleanField(default=False)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('profession', models.CharField(max_length=100, blank=True)),
                ('position', models.CharField(max_length=100, blank=True)),
                ('organization', models.CharField(max_length=2, choices=[(b'1', b'School'), (b'2', b'Think Tank'), (b'3', b'Company'), (b'4', b'Government Agency')])),
                ('organization_name', models.TextField(blank=True)),
                ('forecast_areas', models.CommaSeparatedIntegerField(max_length=3, blank=True)),
                ('forecast_regions', models.CommaSeparatedIntegerField(max_length=3, blank=True)),
                ('activation_token', models.TextField(max_length=256, blank=True)),
                ('expires_at', models.DateTimeField(null=True, blank=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('conditions_accepted', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forecast_type', models.CharField(max_length=2, choices=[('1', b'Binary'), ('2', b'Probability'), ('3', b'Magnitude'), ('4', b'Temporal')])),
                ('forecast_question', models.TextField(max_length=1000)),
                ('start_date', models.DateField(auto_now=True)),
                ('end_date', models.DateField(null=True, blank=True)),
            ],
            options={
                'ordering': ['-end_date'],
                'db_table': 'forecasts',
                'get_latest_by': 'start_date',
            },
        ),
        migrations.CreateModel(
            name='ForecastPropose',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forecast_type_new', models.CharField(max_length=2, choices=[('1', b'Binary'), ('2', b'Probability'), ('3', b'Magnitude'), ('4', b'Temporal')])),
                ('forecast_question_new', models.TextField(max_length=1000)),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(default=b'Unpublished', max_length=1, choices=[(b'u', b'Unpublished'), (b'p', b'Published')])),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ForecastTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forecast_id', models.ForeignKey(to='forecast.Forecast')),
            ],
        ),
        migrations.CreateModel(
            name='ForecastVotes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('forecast_id', models.ForeignKey(related_name='votes', to='forecast.Forecast')),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'forecast vote',
                'verbose_name_plural': 'forecast votes',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='forecasttags',
            name='tag_id',
            field=models.ForeignKey(to='forecast.Tags'),
        ),
    ]
