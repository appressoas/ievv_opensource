# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BulkOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('context_object_id', models.PositiveIntegerField(null=True)),
                ('operationtype', models.CharField(max_length=255, db_index=True, blank=True, default='')),
                ('status', models.CharField(max_length=12, default='unprocessed', choices=[('unprocessed', 'unprocessed'), ('running', 'running'), ('finished', 'finished')])),
                ('result', models.CharField(max_length=12, default='not-available', choices=[('not-available', 'not available yet (processing not finished)'), ('successful', 'successful'), ('failed', 'failed')])),
                ('input_data', models.TextField(blank=True, default='')),
                ('output_data', models.TextField(blank=True, default='')),
                ('context_content_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
                ('started_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
