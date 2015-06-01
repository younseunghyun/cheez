# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import cheez.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_user_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='device',
            name='modified',
            field=cheez.models.AutoDateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='snsaccount',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='snsaccount',
            name='modified',
            field=cheez.models.AutoDateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='user',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='user',
            name='modified',
            field=cheez.models.AutoDateTimeField(default=django.utils.timezone.now),
        ),
    ]
