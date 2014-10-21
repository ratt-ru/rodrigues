# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0003_auto_20141021_1408'),
    ]

    operations = [
        migrations.RenameField(
            model_name='simulation',
            old_name='ima_channelise',
            new_name='channelise',
        ),
        migrations.RenameField(
            model_name='simulation',
            old_name='dc_cleaning',
            new_name='clean',
        ),
        migrations.RenameField(
            model_name='simulation',
            old_name='pointing_errors',
            new_name='cr_pointing_error',
        ),
        migrations.RenameField(
            model_name='simulation',
            old_name='rfi',
            new_name='cr_rfi',
        ),
        migrations.RenameField(
            model_name='simulation',
            old_name='dc_algorithm',
            new_name='dc_operation',
        ),
        migrations.RenameField(
            model_name='simulation',
            old_name='primary_beam',
            new_name='ds_primary_beam',
        ),
        migrations.RenameField(
            model_name='simulation',
            old_name='sky_model',
            new_name='skymodel',
        ),
        migrations.RenameField(
            model_name='simulation',
            old_name='sky_type',
            new_name='skytype',
        ),
        migrations.RenameField(
            model_name='simulation',
            old_name='tdl_conf_file',
            new_name='tdlconf',
        ),
        migrations.RenameField(
            model_name='simulation',
            old_name='tdl_section',
            new_name='tdlsection',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='am_phase_gains',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='corrup_am_phase_gains',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='noise_standard_dev',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='par_angle_rot',
        ),
        migrations.AddField(
            model_name='simulation',
            name='cr_amp_phase_gains',
            field=models.FloatField(default=1, verbose_name=b'Amplitude Phase Gains'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='ds_amp_phase_gains',
            field=models.FloatField(default=1, verbose_name=b'Amplitude Phase Gains'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='ds_feed_angle',
            field=models.FloatField(default=0, verbose_name=b'Feed angle'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='ds_parallactic_angle_rotation',
            field=models.BooleanField(default=True, verbose_name=b'Parallactic Angle Rotation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='vis_noise_std',
            field=models.FloatField(default=0, verbose_name=b'Noise Standard Deviation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='simulation',
            name='name',
            field=models.CharField(default=b'New simulation', max_length=200),
        ),
    ]
