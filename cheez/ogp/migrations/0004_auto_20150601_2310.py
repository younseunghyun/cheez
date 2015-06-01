# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cheez.models


class Migration(migrations.Migration):

    dependencies = [
        ('ogp', '0003_auto_20150601_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='og',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='og',
            name='modified',
            field=cheez.models.AutoDateTimeField(auto_now=True),
        ),
    ]
