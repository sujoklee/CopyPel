# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0002_auto_20150610_1021'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forecastpropose',
            old_name='date',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='forecastpropose',
            old_name='forecast_question_new',
            new_name='forecast_question',
        ),
        migrations.RenameField(
            model_name='forecastpropose',
            old_name='forecast_type_new',
            new_name='forecast_type',
        ),
        migrations.RenameField(
            model_name='forecastpropose',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='forecast',
            name='start_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='forecastpropose',
            name='status',
            field=models.CharField(default=b'u', max_length=1, choices=[(b'u', b'Unpublished'), (b'p', b'Published')]),
        ),
    ]
