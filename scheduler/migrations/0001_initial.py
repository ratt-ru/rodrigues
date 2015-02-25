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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.TextField()),
                ('started', models.DateTimeField(null=True, blank=True)),
                ('finished', models.DateTimeField(null=True, blank=True)),
                ('log', models.TextField(blank=True)),
                ('task_id', models.CharField(max_length=36, null=True, blank=True)),
                ('config', models.TextField()),
                ('docker_image', models.TextField()),
                ('state', models.CharField(default='S', max_length=1, choices=[('S', 'scheduled'), ('R', 'running'), ('C', 'crashed'), ('F', 'finished')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
