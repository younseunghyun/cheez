# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150611_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='state_message',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
