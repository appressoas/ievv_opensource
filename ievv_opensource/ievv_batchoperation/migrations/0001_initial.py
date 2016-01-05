# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchOperation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('started_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('finished_datetime', models.DateTimeField(null=True, blank=True)),
                ('context_object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('operationtype', models.CharField(default='', blank=True, db_index=True, max_length=255)),
                ('status', models.CharField(default='unprocessed', choices=[('unprocessed', 'unprocessed'), ('running', 'running'), ('finished', 'finished')], max_length=12)),
                ('result', models.CharField(default='not-available', choices=[('not-available', 'not available yet (processing not finished)'), ('successful', 'successful'), ('failed', 'failed')], max_length=13)),
                ('input_data_json', models.TextField(default='', blank=True)),
                ('output_data_json', models.TextField(default='', blank=True)),
                ('context_content_type', models.ForeignKey(to='contenttypes.ContentType', blank=True, null=True)),
                ('started_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
        ),
    ]
