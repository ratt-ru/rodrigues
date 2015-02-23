# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('state', models.CharField(default=b'S', max_length=1, choices=[(b'S', b'scheduled'), (b'R', b'running'), (b'C', b'crashed'), (b'F', b'finished')])),
                ('started', models.DateTimeField(null=True, blank=True)),
                ('finished', models.DateTimeField(null=True, blank=True)),
                ('log', models.FileField(null=True, upload_to=b'', blank=True)),
                ('task_id', models.CharField(max_length=36, null=True, blank=True)),
                ('config', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
