# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20150501_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='subtitle',
            field=models.CharField(max_length=512, null=True),
        ),
    ]
