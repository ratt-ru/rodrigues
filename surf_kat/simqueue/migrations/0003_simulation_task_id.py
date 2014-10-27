# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0002_auto_20141027_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='task_id',
            field=models.TextField(max_length=32, blank=True, null=True),
            preserve_default=True,
        ),
    ]
