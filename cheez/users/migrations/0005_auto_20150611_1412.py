# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_state_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='state_message',
            field=models.CharField(null=True, max_length=256, blank=True),
        ),
    ]
