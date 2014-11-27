# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0002_auto_20141126_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='channelise',
            field=models.IntegerField(help_text='0 means average all, 1 per channel, etc.', verbose_name='Image channelise', default=0),
            preserve_default=True,
        ),
    ]
