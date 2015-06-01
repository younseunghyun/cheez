# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ogp', '0004_auto_20150601_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='og',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
