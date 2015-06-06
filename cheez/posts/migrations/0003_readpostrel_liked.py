# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20150604_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='readpostrel',
            name='liked',
            field=models.BooleanField(default=False),
        ),
    ]
