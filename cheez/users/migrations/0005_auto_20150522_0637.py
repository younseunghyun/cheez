# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150522_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='user',
            field=models.ForeignKey(related_name='devices', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='snsaccount',
            name='user',
            field=models.ForeignKey(related_name='sns_accounts', null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
