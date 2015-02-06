# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0003_simulation_results_psf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='moresane_startscale',
            field=models.IntegerField(default=1, verbose_name='Start scale'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='simulation',
            name='moresane_stopscale',
            field=models.IntegerField(default=20, verbose_name='Stop scale'),
            preserve_default=True,
        ),
    ]
