# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0005_auto_20150614_1931'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forecastvotes',
            old_name='forecast_id',
            new_name='forecast',
        ),
    ]
