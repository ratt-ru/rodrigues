# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0006_auto_20141027_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='results_dirty',
            field=models.FileField(null=True, upload_to=b'dirty', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='results_model',
            field=models.FileField(null=True, upload_to=b'model', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='results_residual',
            field=models.FileField(null=True, upload_to=b'residual', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='results_restored',
            field=models.FileField(null=True, upload_to=b'restored', blank=True),
            preserve_default=True,
        ),
    ]
