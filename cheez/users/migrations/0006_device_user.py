# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_device_device_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='user',
            field=models.ForeignKey(default=None, to='users.User'),
            preserve_default=False,
        ),
    ]
