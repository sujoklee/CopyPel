# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0004_auto_20150614_1519'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forecastvotes',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='forecastvotevariant',
            name='forecast',
            field=models.ForeignKey(related_name='variants', to='forecast.Forecast'),
        ),
    ]
