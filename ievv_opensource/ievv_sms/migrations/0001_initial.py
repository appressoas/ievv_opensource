# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-10 13:09
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DebugSmsMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(db_index=True, max_length=50)),
                ('message', models.TextField()),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
