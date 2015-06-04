# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20150601_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='push_token',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
