# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-11-06 13:10
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ievv_logging', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ievvloggingeventbase',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='ievvloggingeventitem',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='ievvloggingeventitem',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ievvloggingeventitem',
            name='time_spent_in_seconds',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
