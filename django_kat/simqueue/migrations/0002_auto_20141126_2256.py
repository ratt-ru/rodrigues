# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='simulation',
            old_name='ms_hours',
            new_name='ms_synthesis',
        ),
        migrations.AddField(
            model_name='simulation',
            name='ms_scan_length',
            field=models.FloatField(blank=True, help_text='in hours', default=0.25, verbose_name='Scan length'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='simulation',
            name='make_psf',
            field=models.BooleanField(default=False, verbose_name='Make PSF'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ms_start_time',
            field=models.FloatField(blank=True, help_text='in hours', default=-0.125, verbose_name='Initial hour angle'),
            preserve_default=True,
        ),
    ]
