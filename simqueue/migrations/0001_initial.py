# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Simulation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'New simulation', max_length=200)),
                ('sky_type', models.CharField(default=b'T', max_length=1, choices=[(b'T', b'Tigger LSM'), (b'F', b'FITS'), (b'S', b'Siamese Model')])),
                ('sky_model', models.FileField(upload_to=b'', blank=True)),
                ('tdl_conf_file', models.FileField(help_text=b'TDL Configuration File', upload_to=b'', blank=True)),
                ('tdl_section', models.CharField(max_length=200, blank=True)),
                ('make_psf', models.BooleanField(default=True)),
                ('add_noise', models.BooleanField(default=True)),
                ('noise_standard_dev', models.FloatField(default=0)),
                ('output', models.CharField(default=b'I', max_length=1, choices=[(b'I', b'Image'), (b'V', b'Visibilities')])),
                ('synthesis_time', models.FloatField(default=1, help_text=b'in seconds')),
                ('integration_time', models.FloatField(default=1, help_text=b'in seconds')),
                ('start_frequency', models.FloatField(default=1, help_text=b'in Hz')),
                ('channel_width', models.FloatField(default=1, help_text=b'in Hz')),
                ('channels_per_band', models.IntegerField(default=1, help_text=b'Number of frequency channels per band')),
                ('freq_bands', models.IntegerField(default=1, help_text=b'Number of frequency bands')),
                ('correlate', models.BooleanField(default=True, help_text=b'Autocorrelation data')),
                ('declination', models.FloatField(null=True, blank=True)),
                ('right_ascension', models.FloatField(null=True, blank=True)),
                ('am_phase_gains', models.FloatField(default=1, help_text=b'Amplitude Phase Gains')),
                ('par_angle_rot', models.BooleanField(default=True, help_text=b'Parallactic Angle Rotation')),
                ('primary_beam', models.CharField(default=b'M', max_length=1, choices=[(b'M', b'MeerKAT 1'), (b'N', b'MeerKAT 2'), (b'O', b'MeerKAT 3'), (b'K', b'KAT-7'), (b'W', b'WSRT'), (b'J', b'JVLA')])),
                ('corrup_am_phase_gains', models.FloatField(default=1, help_text=b'Amplitude Phase Gains')),
                ('pointing_errors', models.FloatField(default=0)),
                ('rfi', models.FloatField(default=0)),
                ('pixels', models.IntegerField(default=1)),
                ('pixel_width', models.FloatField(default=1, help_text=b'in arcseconds')),
                ('uv_weighting', models.CharField(default=b'N', max_length=1, choices=[(b'N', b'Natural'), (b'U', b'Uniform'), (b'B', b'Briggs')])),
                ('weight_fov', models.FloatField(default=1, help_text=b'in arcminutes')),
                ('w_projection_planes', models.IntegerField(default=1)),
                ('imaging_mode', models.CharField(default=b'C', max_length=1, choices=[(b'C', b'Channel'), (b'M', b'MFS')])),
                ('spectral_window', models.FloatField(default=1)),
                ('num_channels', models.IntegerField(default=1)),
                ('image_channelise', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Average all'), (b'E', b'Image every channel'), (b'C', b'Custom')])),
                ('stokes', models.CharField(default=b'Q', max_length=5)),
                ('cleaning', models.BooleanField(default=True)),
                ('Deconv_alg', models.CharField(default=b'c', max_length=1, choices=[(b'C', b'csclean'), (b'H', b'hogbom'), (b'D', b'clark'), (b'M', b'multiscale')])),
                ('clean_scales', models.FloatField(default=1)),
                ('num_scales', models.FloatField(default=1)),
                ('num_clean_iter', models.IntegerField(default=1, help_text=b'number of clean iterations')),
                ('clean_threshold', models.FloatField(default=1, help_text=b'in mJy')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
