# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20150522_0639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='devices'),
        ),
        migrations.AlterField(
            model_name='snsaccount',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='sns_accounts'),
        ),
    ]
