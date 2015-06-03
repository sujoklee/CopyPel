# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forecast', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForecastAnalysis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('body', models.TextField(max_length=1000, null=True, blank=True)),
                ('forecast', models.ForeignKey(to='forecast.Forecast')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ForecastMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('url', models.URLField()),
                ('image', models.ImageField(upload_to=b'')),
                ('forecast', models.ForeignKey(to='forecast.Forecast')),
            ],
        ),
    ]
