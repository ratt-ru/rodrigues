# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_job_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['started']},
        ),
        migrations.AlterField(
            model_name='job',
            name='state',
            field=models.CharField(max_length=1, default='I', choices=[('I', 'CREATED'), ('S', 'SCHEDULED'), ('R', 'RUNNING'), ('C', 'CRASHED'), ('F', 'FINISHED')]),
        ),
    ]
