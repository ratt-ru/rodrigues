# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0004_auto_20141027_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='results_uvcov',
            field=models.FileField(null=True, upload_to=b'uvcov', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='simulation',
            name='sky_model',
            field=models.FileField(upload_to=b'sky', blank=True),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='tdl_conf',
            field=models.FileField(upload_to=b'tdl', verbose_name=b'TDL Configuration File', blank=True),
        ),
    ]
