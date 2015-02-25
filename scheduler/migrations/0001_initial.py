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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('started', models.DateTimeField(null=True, blank=True)),
                ('finished', models.DateTimeField(null=True, blank=True)),
                ('log', models.TextField(blank=True)),
                ('task_id', models.CharField(null=True, blank=True, max_length=36)),
                ('config', models.TextField()),
                ('docker_image', models.TextField()),
                ('results_dir', models.TextField()),
                ('state', models.CharField(default='S', choices=[('S', 'scheduled'), ('R', 'running'), ('C', 'crashed'), ('F', 'finished')], max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
