# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20150522_0637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='devices', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='snsaccount',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='sns_accounts', default=1),
            preserve_default=False,
        ),
    ]
