# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0008_auto_20150614_2128'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForecastVoteChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField(unique=True)),
                ('choice', models.CharField(max_length=150)),
                ('forecast', models.ForeignKey(related_name='choices', to='forecast.Forecast')),
            ],
        ),
        migrations.RemoveField(
            model_name='forecastvotevariant',
            name='forecast',
        ),
        migrations.RemoveField(
            model_name='forecastvotes',
            name='variant',
        ),
        migrations.DeleteModel(
            name='ForecastVoteVariant',
        ),
        migrations.AddField(
            model_name='forecastvotes',
            name='choice',
            field=models.ForeignKey(blank=True, to='forecast.ForecastVoteChoice', null=True),
        ),
    ]
