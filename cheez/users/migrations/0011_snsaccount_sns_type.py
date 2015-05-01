# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_snsaccount_sns_profile_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='snsaccount',
            name='sns_type',
            field=models.IntegerField(choices=[(1, 'FACEBOOK')], default=1),
        ),
    ]
