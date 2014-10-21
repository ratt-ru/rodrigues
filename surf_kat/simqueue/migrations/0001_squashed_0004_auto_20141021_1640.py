# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [(b'simqueue', '0001_initial'), (b'simqueue', '0002_simulation_task_id'), (b'simqueue', '0003_auto_20141021_1408'), (b'simqueue', '0004_auto_20141021_1640')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Simulation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'New simulation', max_length=200)),
                ('skytype', models.CharField(default=b'T', max_length=1, choices=[(b'T', b'Tigger LSM'), (b'F', b'FITS'), (b'S', b'Siamese Model')])),
                ('skymodel', models.FileField(upload_to=b'', blank=True)),
                ('tdlconf', models.FileField(help_text=b'TDL Configuration File', upload_to=b'', blank=True)),
                ('tdlsection', models.CharField(max_length=200, blank=True)),
                ('make_psf', models.BooleanField(default=True)),
                ('add_noise', models.BooleanField(default=True)),
                ('output', models.CharField(default=b'I', max_length=1, verbose_name=b'Output type', choices=[(b'I', b'Image'), (b'V', b'Visibilities')])),
                ('ds_primary_beam', models.CharField(default=b'M', max_length=1, choices=[(b'M', b'MeerKAT 1'), (b'N', b'MeerKAT 2'), (b'O', b'MeerKAT 3'), (b'K', b'KAT-7'), (b'W', b'WSRT'), (b'J', b'JVLA')])),
                ('cr_pointing_error', models.FloatField(default=0)),
                ('cr_rfi', models.FloatField(default=0)),
                ('state', models.CharField(default=b'S', max_length=1, choices=[(b'S', b'scheduled'), (b'R', b'running'), (b'T', b'stopped'), (b'A', b'aborted'), (b'C', b'crashed'), (b'F', b'finished')])),
                ('started', models.DateTimeField(null=True, blank=True)),
                ('finished', models.DateTimeField(null=True, blank=True)),
                ('log', models.TextField(null=True, blank=True)),
                ('task_id', models.CharField(max_length=36, null=True, blank=True)),
                ('dc_operation', models.CharField(default=b'C', max_length=1, verbose_name=b'Deconvolution Algorithm', choices=[(b'C', b'csclean'), (b'H', b'hogbom'), (b'D', b'clark'), (b'M', b'multiscale'), (b'S', b'MORESANE')])),
                ('clean', models.BooleanField(default=True, verbose_name=b'Deconvolve')),
                ('dc_niter', models.IntegerField(default=1000, help_text=b'number of clean iterations', verbose_name=b'Clean Iterations')),
                ('dc_nscales', models.FloatField(default=4, verbose_name=b'Scales to clean')),
                ('dc_threshold', models.FloatField(default=0, help_text=b'in mJy', verbose_name=b'Clean threshold')),
                ('dc_uservector', models.CharField(default=b'0 1 4 8 16 64 128', help_text=b'List of scales to clean', max_length=64, verbose_name=b'Clean scales')),
                ('im_cellsize', models.FloatField(default=1, help_text=b'in arcseconds', verbose_name=b'Pixel size')),
                ('im_mode', models.CharField(default=b'C', max_length=1, verbose_name=b'Imaging mode', choices=[(b'C', b'Channel'), (b'M', b'MFS')])),
                ('im_npix', models.IntegerField(default=512, help_text=b'in pixels', verbose_name=b'Image size')),
                ('im_spwid', models.CharField(default=1, max_length=32, verbose_name=b'Spectral window')),
                ('im_stokes', models.CharField(default=b'I', max_length=4, verbose_name=b'Stokes')),
                ('im_weight', models.CharField(default=b'N', max_length=1, verbose_name=b'uv-Weighting', choices=[(b'N', b'Natural'), (b'U', b'Uniform'), (b'B', b'Briggs')])),
                ('im_weight_fov', models.FloatField(default=1, help_text=b'in arcminutes', verbose_name=b'Weight FoV')),
                ('im_wprojplanes', models.IntegerField(default=0, verbose_name=b'w-Projection planes')),
                ('channelise', models.CharField(default=b'A', max_length=1, verbose_name=b'Image channelise', choices=[(b'A', b'Average all'), (b'E', b'Image every channel'), (b'C', b'Custom')])),
                ('ms_dec', models.FloatField(null=True, verbose_name=b'Declinations', blank=True)),
                ('ms_dfreq', models.FloatField(default=1, help_text=b'in Hz', verbose_name=b'Channel width')),
                ('ms_dtime', models.FloatField(default=1, help_text=b'in seconds', verbose_name=b'Integration time')),
                ('ms_freq0', models.FloatField(default=1, help_text=b'in Hz', verbose_name=b'Start frequency')),
                ('ms_hours', models.FloatField(default=1, help_text=b'in seconds', verbose_name=b'Synthesis time')),
                ('ms_nband', models.IntegerField(default=1, help_text=b'Number of frequency bands', verbose_name=b'Frequency bands')),
                ('ms_nchan', models.IntegerField(default=1, help_text=b'Number of frequency channels per band', verbose_name=b'Channels per band')),
                ('ms_ra', models.FloatField(null=True, verbose_name=b'Right ascension', blank=True)),
                ('ms_writeAutoCorr', models.BooleanField(default=True, help_text=b'Include autocorrelation in data', verbose_name=b'Autocorrelations')),
                ('cr_amp_phase_gains', models.FloatField(default=1, verbose_name=b'Amplitude Phase Gains')),
                ('ds_amp_phase_gains', models.FloatField(default=1, verbose_name=b'Amplitude Phase Gains')),
                ('ds_feed_angle', models.FloatField(default=0, verbose_name=b'Feed angle')),
                ('ds_parallactic_angle_rotation', models.BooleanField(default=True, verbose_name=b'Parallactic Angle Rotation')),
                ('vis_noise_std', models.FloatField(default=0, verbose_name=b'Noise Standard Deviation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
