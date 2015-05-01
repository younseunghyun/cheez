# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_snsaccount_sns_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='snsaccount',
            name='sns_user_id',
            field=models.CharField(max_length=128, default=None),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='snsaccount',
            unique_together=set([('sns_type', 'sns_user_id')]),
        ),
    ]
