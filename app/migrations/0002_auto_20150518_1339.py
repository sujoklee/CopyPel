# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
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
                ('forecast_areas', models.CommaSeparatedIntegerField(max_length=3, blank=True)),
                ('forecast_regions', models.CommaSeparatedIntegerField(max_length=3, blank=True)),
                ('activation_token', models.TextField(blank=True)),
                ('expires_at', models.DateTimeField(blank=True)),
                ('email_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AlterField(
            model_name='forecastvotes',
            name='user_id',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelTable(
            name='organization',
            table='organization',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
        migrations.AddField(
            model_name='customuserprofile',
            name='organization',
            field=models.ForeignKey(to='app.Organization', blank=True),
        ),
        migrations.AddField(
            model_name='customuserprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
