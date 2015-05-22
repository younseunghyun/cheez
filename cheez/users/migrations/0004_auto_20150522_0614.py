# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150522_0614'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='device',
            unique_together=set([('os_type', 'device_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='snsaccount',
            unique_together=set([('sns_type', 'sns_user_id')]),
        ),
    ]
