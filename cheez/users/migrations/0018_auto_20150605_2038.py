# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_device_push_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followee_count',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='follower_count',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
