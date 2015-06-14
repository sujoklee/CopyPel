# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0006_auto_20150614_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecastvotevariant',
            name='num',
            field=models.IntegerField(unique=True),
        ),
    ]
