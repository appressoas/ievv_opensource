# -*- coding: utf-8 -*-
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ievv_batchframework', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='batchoperation',
            options={'ordering': ['-created_datetime']},
        ),
    ]
