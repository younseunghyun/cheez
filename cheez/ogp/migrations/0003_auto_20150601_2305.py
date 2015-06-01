# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import cheez.models


class Migration(migrations.Migration):

    dependencies = [
        ('ogp', '0002_auto_20150520_0718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='og',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='og',
            name='modified',
            field=cheez.models.AutoDateTimeField(default=django.utils.timezone.now),
        ),
    ]
