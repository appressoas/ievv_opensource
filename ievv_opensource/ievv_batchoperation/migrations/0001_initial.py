# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


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
                ('context_object_id', models.PositiveIntegerField(null=True)),
                ('operationtype', models.CharField(blank=True, db_index=True, default='', max_length=255)),
                ('status', models.CharField(choices=[('unprocessed', 'unprocessed'), ('running', 'running'), ('finished', 'finished')], default='unprocessed', max_length=12)),
                ('result', models.CharField(choices=[('not-available', 'not available yet (processing not finished)'), ('successful', 'successful'), ('failed', 'failed')], default='not-available', max_length=12)),
                ('input_data_json', models.TextField(default='', blank=True)),
                ('output_data_json', models.TextField(default='', blank=True)),
                ('context_content_type', models.ForeignKey(null=True, to='contenttypes.ContentType')),
                ('started_by', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
