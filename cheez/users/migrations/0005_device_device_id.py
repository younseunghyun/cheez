# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='device_id',
            field=models.CharField(unique=True, max_length=512, default=None),
            preserve_default=False,
        ),
    ]
