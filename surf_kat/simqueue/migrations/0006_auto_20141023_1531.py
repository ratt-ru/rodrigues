# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0005_auto_20141022_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simulation',
            name='task_id',
        ),
        migrations.AlterField(
            model_name='simulation',
            name='im_spwid',
            field=models.CharField(default=0, max_length=32, verbose_name=b'Spectral window'),
        ),
    ]
