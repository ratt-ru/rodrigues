# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='channelise',
            field=models.CharField(verbose_name='Image channelise', choices=[('NCHAN', 'Average all'), ('1', 'Image every channel'), ('custom', 'Custom')], default='A', max_length=10),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='cr_amp_phase_gains',
            field=models.FloatField(default=1, verbose_name='Amplitude Phase Gains'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='dc_niter',
            field=models.IntegerField(help_text='number of clean iterations', default=1000, verbose_name='Clean Iterations'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='dc_nscales',
            field=models.FloatField(default=4, verbose_name='Scales to clean'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='dc_operation',
            field=models.CharField(verbose_name='Deconvolution Algorithm', choices=[('C', 'csclean'), ('H', 'hogbom'), ('D', 'clark'), ('M', 'multiscale'), ('S', 'MORESANE')], default='C', max_length=1),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='dc_threshold',
            field=models.FloatField(help_text='in mJy', default=0, verbose_name='Clean threshold'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='dc_uservector',
            field=models.CharField(help_text='List of scales to clean', verbose_name='Clean scales', default='0 1 4 8 16 64 128', max_length=64),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='deconvolve',
            field=models.BooleanField(default=True, verbose_name='Deconvolve'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ds_amp_phase_gains',
            field=models.FloatField(default=1, verbose_name='Amplitude Phase Gains'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ds_feed_angle',
            field=models.FloatField(default=0, verbose_name='Feed angle'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ds_parallactic_angle_rotation',
            field=models.BooleanField(default=True, verbose_name='Parallactic Angle Rotation'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ds_primary_beam',
            field=models.CharField(choices=[('M', 'MeerKAT 1'), ('N', 'MeerKAT 2'), ('O', 'MeerKAT 3'), ('K', 'KAT-7'), ('W', 'WSRT'), ('J', 'JVLA')], default='M', max_length=1),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='im_cellsize',
            field=models.FloatField(help_text='in arcseconds', default=1, verbose_name='Pixel size'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='im_mode',
            field=models.CharField(verbose_name='Imaging mode', choices=[('C', 'Channel'), ('M', 'MFS')], default='C', max_length=1),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='im_npix',
            field=models.IntegerField(help_text='in pixels', default=512, verbose_name='Image size'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='im_spwid',
            field=models.CharField(verbose_name='Spectral window', default=0, max_length=32),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='im_stokes',
            field=models.CharField(verbose_name='Stokes', default='I', max_length=4),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='im_weight',
            field=models.CharField(verbose_name='uv-Weighting', choices=[('N', 'Natural'), ('U', 'Uniform'), ('B', 'Briggs')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='im_weight_fov',
            field=models.FloatField(help_text='in arcminutes', default=1, verbose_name='Weight FoV'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='im_wprojplanes',
            field=models.IntegerField(default=0, verbose_name='w-Projection planes'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ms_dec',
            field=models.FloatField(default=-30, verbose_name='Declinations'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ms_dfreq',
            field=models.FloatField(help_text='in Hz', default=50000000.0, verbose_name='Channel width'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ms_dtime',
            field=models.IntegerField(help_text='in seconds', default=10, verbose_name='Integration time'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ms_freq0',
            field=models.FloatField(help_text='in Hz', default=1400000000.0, verbose_name='Start frequency'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ms_hours',
            field=models.IntegerField(help_text='in hours', default=4, verbose_name='Synthesis time'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ms_nband',
            field=models.IntegerField(help_text='Number of frequency bands', default=1, verbose_name='Frequency bands'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ms_nchan',
            field=models.IntegerField(help_text='Number of frequency channels per band', default=1, verbose_name='Channels per band'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ms_ra',
            field=models.FloatField(default=0, verbose_name='Right ascension'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='ms_write_auto_corr',
            field=models.BooleanField(help_text='Include autocorrelation in data', default=True, verbose_name='Autocorrelations'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='name',
            field=models.CharField(default='New simulation', max_length=200),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='output',
            field=models.CharField(verbose_name='Output type', choices=[('I', 'Image'), ('V', 'Visibilities')], default='I', max_length=1),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='sky_model',
            field=models.FileField(upload_to='', blank=True),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='sky_type',
            field=models.CharField(choices=[('T', 'Tigger LSM'), ('F', 'FITS'), ('S', 'Siamese Model')], default='T', max_length=1),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='state',
            field=models.CharField(choices=[('S', 'scheduled'), ('R', 'running'), ('T', 'stopped'), ('A', 'aborted'), ('C', 'crashed'), ('F', 'finished')], default='S', max_length=1),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='tdl_conf',
            field=models.FileField(help_text='TDL Configuration File', upload_to='', blank=True),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='vis_noise_std',
            field=models.FloatField(default=0, verbose_name='Noise Standard Deviation'),
        ),
    ]
