# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0002_auto_20141021_1646'),
    ]

    operations = [
        migrations.RenameField(
            model_name='simulation',
            old_name='ms_writeAutoCorr',
            new_name='ms_write_auto_corr',
        ),
        migrations.RenameField(
            model_name='simulation',
            old_name='skymodel',
            new_name='sky_model',
        ),
        migrations.RenameField(
            model_name='simulation',
            old_name='skytype',
            new_name='sky_type',
        ),
        migrations.RenameField(
            model_name='simulation',
            old_name='tdlconf',
            new_name='tdl_conf',
        ),
        migrations.RenameField(
            model_name='simulation',
            old_name='tdlsection',
            new_name='tdl_section',
        ),
        migrations.AlterField(
            model_name='simulation',
            name='channelise',
            field=models.CharField(default=b'A', max_length=10, verbose_name=b'Image channelise', choices=[(b'NCHAN', b'Average all'), (b'1', b'Image every channel'), (b'custom', b'Custom')]),
        ),
    ]
