# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0004_auto_20141022_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='ms_dfreq',
            field=models.FloatField(default=50000000.0, help_text=b'in Hz', verbose_name=b'Channel width'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ms_dtime',
            field=models.IntegerField(default=10, help_text=b'in seconds', verbose_name=b'Integration time'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ms_freq0',
            field=models.FloatField(default=1400000000.0, help_text=b'in Hz', verbose_name=b'Start frequency'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ms_hours',
            field=models.IntegerField(default=4, help_text=b'in hours', verbose_name=b'Synthesis time'),
        ),
    ]
