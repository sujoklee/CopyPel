# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0002_group_membership'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForecastVoteVariant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField()),
                ('value', models.CharField(max_length=150)),
                ('forecast', models.ForeignKey(to='forecast.Forecast')),
            ],
        ),
    ]
