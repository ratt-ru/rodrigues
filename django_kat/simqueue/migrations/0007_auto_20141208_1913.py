# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simqueue', '0006_auto_20141203_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='casa_sigmalevel',
            field=models.FloatField(default=0, verbose_name='Clean sigma level', help_text='In sigma above noise'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='lwimager_sigmalevel',
            field=models.FloatField(default=0, verbose_name='Clean sigma level', help_text='In sigma above noise'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simulation',
            name='wsclean_sigmalevel',
            field=models.FloatField(default=0, verbose_name='Clean sigma level', help_text='In sigma above noise'),
            preserve_default=True,
        ),
    ]
