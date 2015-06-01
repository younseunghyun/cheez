# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cheez.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20150601_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='modified',
            field=cheez.models.AutoDateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='modified',
            field=cheez.models.AutoDateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='readpostrel',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='readpostrel',
            name='modified',
            field=cheez.models.AutoDateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='modified',
            field=cheez.models.AutoDateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='modified',
            field=cheez.models.AutoDateTimeField(auto_now=True),
        ),
    ]
