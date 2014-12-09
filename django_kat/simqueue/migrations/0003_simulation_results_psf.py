# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0002_simulation_results_dirty'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='results_psf',
            field=models.FileField(blank=True, null=True, upload_to='psf'),
            preserve_default=True,
        ),
    ]
