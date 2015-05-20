# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ogp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='og',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]
