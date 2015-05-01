# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_snsaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='snsaccount',
            name='user',
            field=models.ForeignKey(default=None, to='users.User'),
            preserve_default=False,
        ),
    ]
