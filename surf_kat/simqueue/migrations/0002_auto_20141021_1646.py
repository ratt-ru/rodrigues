# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0001_squashed_0004_auto_20141021_1640'),
    ]

    operations = [
        migrations.RenameField(
            model_name='simulation',
            old_name='clean',
            new_name='deconvolve',
        ),
    ]
