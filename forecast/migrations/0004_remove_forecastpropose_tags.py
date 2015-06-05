# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0003_forecastpropose_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forecastpropose',
            name='tags',
        ),
    ]
