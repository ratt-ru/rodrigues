# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0005_auto_20141027_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='task_id',
            field=models.CharField(max_length=36, null=True, blank=True),
        ),
    ]
