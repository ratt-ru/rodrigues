# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0007_auto_20141027_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='ms_hours',
            field=models.FloatField(default=0.25, help_text=b'in hours', verbose_name=b'Synthesis time'),
            preserve_default=True,
        ),
    ]
