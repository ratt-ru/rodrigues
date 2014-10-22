# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0003_auto_20141022_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='ms_dec',
            field=models.FloatField(default=-30, verbose_name=b'Declinations'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ms_ra',
            field=models.FloatField(default=0, verbose_name=b'Right ascension'),
        ),
    ]
