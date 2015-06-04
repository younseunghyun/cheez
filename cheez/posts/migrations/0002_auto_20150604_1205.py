# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='readpostrel',
            name='link_closed_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='readpostrel',
            name='link_opened_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='readpostrel',
            name='view_ended_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='readpostrel',
            name='view_started_time',
            field=models.IntegerField(default=0),
        ),
    ]
