# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('forecast', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forecasttags',
            name='forecast_id',
        ),
        migrations.RemoveField(
            model_name='forecasttags',
            name='tag_id',
        ),
        migrations.AddField(
            model_name='forecast',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.DeleteModel(
            name='ForecastTags',
        ),
        migrations.DeleteModel(
            name='Tags',
        ),
    ]
