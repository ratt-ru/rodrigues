# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0005_auto_20141202_1147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simulation',
            name='make_psf',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='results_casa_dirty',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='results_lwimager_dirty',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='results_moresane_dirty',
        ),
        migrations.RemoveField(
            model_name='simulation',
            name='results_wsclean_dirty',
        ),
    ]
