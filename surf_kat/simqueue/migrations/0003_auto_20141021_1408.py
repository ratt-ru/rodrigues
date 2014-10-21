# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0002_simulation_task_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simulation',
            name='Deconv_alg',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='channel_width',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='channels_per_band',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='clean_scales',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='clean_threshold',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='cleaning',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='correlate',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='declination',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='freq_bands',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='image_channelise',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='imaging_mode',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='integration_time',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='num_channels',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='num_clean_iter',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='num_scales',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='pixel_width',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='pixels',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='right_ascension',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='spectral_window',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='start_frequency',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='stokes',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='synthesis_time',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='uv_weighting',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='w_projection_planes',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='weight_fov',
        ),
        migrations.AddField(
            model_name='simulation',
            name='dc_algorithm',
            field=models.CharField(default=b'C', max_length=1, verbose_name=b'Deconvolution Algorithm', choices=[(b'C', b'csclean'), (b'H', b'hogbom'), (b'D', b'clark'), (b'M', b'multiscale'), (b'S', b'MORESANE')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='dc_cleaning',
            field=models.BooleanField(default=True, verbose_name=b'Deconvolve'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='dc_niter',
            field=models.IntegerField(default=1000, help_text=b'number of clean iterations', verbose_name=b'Clean Iterations'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='dc_nscales',
            field=models.FloatField(default=4, verbose_name=b'Scales to clean'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='dc_threshold',
            field=models.FloatField(default=0, help_text=b'in mJy', verbose_name=b'Clean threshold'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='dc_uservector',
            field=models.CharField(default=b'0 1 4 8 16 64 128', help_text=b'List of scales to clean', max_length=64, verbose_name=b'Clean scales'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='im_cellsize',
            field=models.FloatField(default=1, help_text=b'in arcseconds', verbose_name=b'Pixel size'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='im_mode',
            field=models.CharField(default=b'C', max_length=1, verbose_name=b'Imaging mode', choices=[(b'C', b'Channel'), (b'M', b'MFS')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='im_npix',
            field=models.IntegerField(default=512, help_text=b'in pixels', verbose_name=b'Image size'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='im_spwid',
            field=models.CharField(default=1, max_length=32, verbose_name=b'Spectral window'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='im_stokes',
            field=models.CharField(default=b'I', max_length=4, verbose_name=b'Stokes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='im_weight',
            field=models.CharField(default=b'N', max_length=1, verbose_name=b'uv-Weighting', choices=[(b'N', b'Natural'), (b'U', b'Uniform'), (b'B', b'Briggs')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='im_weight_fov',
            field=models.FloatField(default=1, help_text=b'in arcminutes', verbose_name=b'Weight FoV'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='im_wprojplanes',
            field=models.IntegerField(default=0, verbose_name=b'w-Projection planes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='ima_channelise',
            field=models.CharField(default=b'A', max_length=1, verbose_name=b'Image channelise', choices=[(b'A', b'Average all'), (b'E', b'Image every channel'), (b'C', b'Custom')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='ms_dec',
            field=models.FloatField(null=True, verbose_name=b'Declinations', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='ms_dfreq',
            field=models.FloatField(default=1, help_text=b'in Hz', verbose_name=b'Channel width'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='ms_dtime',
            field=models.FloatField(default=1, help_text=b'in seconds', verbose_name=b'Integration time'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='ms_freq0',
            field=models.FloatField(default=1, help_text=b'in Hz', verbose_name=b'Start frequency'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='ms_hours',
            field=models.FloatField(default=1, help_text=b'in seconds', verbose_name=b'Synthesis time'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='ms_nband',
            field=models.IntegerField(default=1, help_text=b'Number of frequency bands', verbose_name=b'Frequency bands'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='ms_nchan',
            field=models.IntegerField(default=1, help_text=b'Number of frequency channels per band', verbose_name=b'Channels per band'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='ms_ra',
            field=models.FloatField(null=True, verbose_name=b'Right ascension', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='ms_writeAutoCorr',
            field=models.BooleanField(default=True, help_text=b'Include autocorrelation in data', verbose_name=b'Autocorrelations'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='simulation',
            name='name',
            field=models.CharField(default=b'New simulation', max_length=200, verbose_name=b'Name'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='output',
            field=models.CharField(default=b'I', max_length=1, verbose_name=b'Output type', choices=[(b'I', b'Image'), (b'V', b'Visibilities')]),
        ),
    ]
