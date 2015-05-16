# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150505_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_id',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(null=True, max_length=126, unique=True),
        ),
    ]
