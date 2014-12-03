# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='results_dirty',
            field=models.FileField(blank=True, upload_to='dirty', null=True),
            preserve_default=True,
        ),
    ]
