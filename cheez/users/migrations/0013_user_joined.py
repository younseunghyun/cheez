# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20150526_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='joined',
            field=models.BooleanField(default=False),
        ),
    ]
