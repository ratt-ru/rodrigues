# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0004_auto_20141202_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='moresane_edgeoffset',
            field=models.IntegerField(verbose_name='Edge offset', default=0),
            preserve_default=True,
        ),
    ]
