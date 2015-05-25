# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20150524_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='readpostrel',
            name='saved',
            field=models.BooleanField(default=False),
        ),
    ]
