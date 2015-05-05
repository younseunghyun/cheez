# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='os_type',
            field=models.IntegerField(default=1, choices=[(1, 'ANDROID'), (2, 'IOS')]),
        ),
        migrations.AddField(
            model_name='device',
            name='os_version',
            field=models.CharField(null=True, max_length=64),
        ),
        migrations.AlterUniqueTogether(
            name='device',
            unique_together=set([('os_type', 'device_id')]),
        ),
    ]
