# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchOperation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('started_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('finished_datetime', models.DateTimeField(null=True, blank=True)),
                ('context_object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('operationtype', models.CharField(default='', db_index=True, max_length=255, blank=True)),
                ('status', models.CharField(default='unprocessed', max_length=12, choices=[('unprocessed', 'unprocessed'), ('running', 'running'), ('finished', 'finished')])),
                ('result', models.CharField(default='not-available', max_length=13, choices=[('not-available', 'not available yet (processing not finished)'), ('successful', 'successful'), ('failed', 'failed')])),
                ('input_data_json', models.TextField(default='', blank=True)),
                ('output_data_json', models.TextField(default='', blank=True)),
                ('context_content_type', models.ForeignKey(to='contenttypes.ContentType', null=True, blank=True)),
                ('started_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
            ],
        ),
    ]
