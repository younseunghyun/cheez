# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_snsaccount_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='snsaccount',
            name='sns_profile_url',
            field=models.URLField(null=True),
        ),
    ]
