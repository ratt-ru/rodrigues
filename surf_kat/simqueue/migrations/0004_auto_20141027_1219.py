# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0003_simulation_task_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='result_dir',
            field=models.CharField(max_length=11, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='simulation',
            name='task_id',
            field=models.TextField(max_length=36, null=True, blank=True),
        ),
    ]
