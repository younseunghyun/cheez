# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cheez.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20150601_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='modified',
            field=cheez.models.AutoDateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='snsaccount',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='snsaccount',
            name='modified',
            field=cheez.models.AutoDateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='modified',
            field=cheez.models.AutoDateTimeField(auto_now=True),
        ),
    ]
