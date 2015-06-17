# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0009_auto_20150614_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecastanalysis',
            name='forecast',
            field=models.ForeignKey(related_name='analysis', to='forecast.Forecast'),
        ),
    ]
