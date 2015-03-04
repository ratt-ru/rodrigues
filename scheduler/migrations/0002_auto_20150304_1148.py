# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='docker_image',
            field=models.CharField(blank=True, max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='results_dir',
            field=models.CharField(blank=True, max_length=20, null=True),
            preserve_default=True,
        ),
    ]
