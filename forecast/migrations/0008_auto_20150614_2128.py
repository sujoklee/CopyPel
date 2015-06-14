# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0007_auto_20150614_2004'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forecastvotevariant',
            old_name='value',
            new_name='variant',
        ),
    ]
