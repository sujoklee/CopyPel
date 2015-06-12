# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forecast', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=300, null=True, blank=True)),
                ('type', models.CharField(max_length=1, choices=[(b'1', b'Public'), (b'2', b'Private')])),
                ('organization_type', models.CharField(blank=True, max_length=1, null=True, choices=[(b'1', b'School'), (b'2', b'Think Tank'), (b'3', b'Company'), (b'4', b'Government Agency')])),
                ('region', models.CharField(blank=True, max_length=1, null=True, choices=[(b'1', b'Europe'), (b'2', b'Middle East'), (b'3', b'Africa'), (b'4', b'Asia'), (b'5', b'South Pacific'), (b'6', b'North America'), (b'7', b'South America')])),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('admin_rights', models.BooleanField()),
                ('track_forecasts', models.BooleanField()),
                ('group', models.ForeignKey(to='forecast.Group')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
