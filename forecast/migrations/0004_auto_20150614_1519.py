# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0003_forecastvotevariant'),
    ]

    operations = [
        migrations.AddField(
            model_name='forecastvotes',
            name='variant',
            field=models.ForeignKey(blank=True, to='forecast.ForecastVoteVariant', null=True),
        ),
        migrations.AddField(
            model_name='forecastvotes',
            name='vote2',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='forecast_type',
            field=models.CharField(max_length=2, choices=[(b'1', b'Finite Event'), (b'2', b'Probability'), (b'3', b'Magnitude'), (b'4', b'Time Horizon Event')]),
        ),
        migrations.AlterField(
            model_name='forecastpropose',
            name='forecast_type',
            field=models.CharField(max_length=2, choices=[(b'1', b'Finite Event'), (b'2', b'Probability'), (b'3', b'Magnitude'), (b'4', b'Time Horizon Event')]),
        ),
        migrations.AlterField(
            model_name='forecastvotes',
            name='vote',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
