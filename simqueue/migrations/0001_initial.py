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
                ('sky_type', models.CharField(max_length=1, choices=[(b'T', b'Tigger LSM'), (b'F', b'FITS'), (b'S', b'Siamese Model')])),
                ('sky_model', models.FileField(upload_to=b'')),
                ('upload_tdl', models.BooleanField(default=False)),
                ('tdl_conf_file', models.FileField(help_text=b'TDL Configuration File', upload_to=b'')),
                ('tdl_section', models.TextField()),
                ('make_psf', models.BooleanField(default=False)),
                ('add_noise', models.BooleanField(default=False)),
                ('noise_standard_dev', models.FloatField()),
                ('output', models.CharField(max_length=1, choices=[(b'I', b'Image'), (b'V', b'Visibilities')])),
                ('synthesis_time', models.FloatField()),
                ('integration_time', models.FloatField()),
                ('start_frequency', models.FloatField()),
                ('channel_width', models.FloatField()),
                ('channels_per_band', models.IntegerField(help_text=b'Number of frequency channels per band')),
                ('freq_bands', models.IntegerField(help_text=b'Number of frequency bands')),
                ('correlate', models.BooleanField(default=False, help_text=b'Autocorrelation data')),
                ('declination', models.FloatField()),
                ('right_ascension', models.FloatField()),
                ('am_phase_gains', models.FloatField(verbose_name=b'Amplitude Phase Gains')),
                ('par_angle_rot', models.BooleanField(default=False, help_text=b'Parallactic Angle Rotation')),
                ('primary_beam', models.CharField(max_length=1, choices=[(b'M', b'MeerKAT 1'), (b'N', b'MeerKAT 2'), (b'O', b'MeerKAT 3'), (b'K', b'KAT-7'), (b'W', b'WSRT'), (b'J', b'JVLA')])),
                ('corrup_am_phase_gains', models.FloatField(verbose_name=b'Amplitude Phase Gains')),
                ('pointing_errors', models.FloatField()),
                ('rfi', models.FloatField()),
                ('pixels', models.IntegerField()),
                ('pixel_width', models.FloatField(help_text=b'in arcseconds')),
                ('uv_weighting', models.CharField(max_length=1, choices=[(b'N', b'Natural'), (b'U', b'Uniform'), (b'B', b'Briggs')])),
                ('weight_fov', models.FloatField(help_text=b'in arcminutes')),
                ('w_projection_planes', models.IntegerField()),
                ('imaging_mode', models.CharField(max_length=1, choices=[(b'C', b'Channel'), (b'M', b'MFS')])),
                ('spectral_window', models.FloatField()),
                ('num_channels', models.IntegerField()),
                ('image_channelise', models.CharField(max_length=1, choices=[(b'A', b'Average all'), (b'E', b'Image every channel'), (b'C', b'Custom')])),
                ('stokes', models.TextField()),
                ('clean', models.BooleanField(default=False)),
                ('Deconv_alg', models.CharField(max_length=1, choices=[(b'C', b'csclean'), (b'H', b'hogbom'), (b'D', b'clark'), (b'M', b'multiscale')])),
                ('clean_scales', models.FloatField()),
                ('num_scales', models.FloatField()),
                ('num_clean_iter', models.IntegerField(help_text=b'number of clean iterations')),
                ('clean_threshold', models.FloatField(help_text=b'in mJy')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
