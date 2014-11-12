# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0008_auto_20141110_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='console',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='simulation',
            name='state',
            field=models.CharField(default=b'S', max_length=1, choices=[(b'S', b'scheduled'), (b'R', b'running'), (b'C', b'crashed'), (b'F', b'finished')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='simulation',
            name='tdl_section',
            field=models.CharField(default=b'turbo-sim:default', max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
