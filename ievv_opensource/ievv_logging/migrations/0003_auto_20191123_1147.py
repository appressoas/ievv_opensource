# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-23 11:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ievv_logging', '0002_auto_20191106_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='ievvloggingeventbase',
            name='error_occured',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='ievvloggingeventitem',
            name='error_occured',
            field=models.NullBooleanField(default=None),
        ),
    ]