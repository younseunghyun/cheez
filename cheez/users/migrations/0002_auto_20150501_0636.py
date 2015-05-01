# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='created',
        ),
        migrations.RemoveField(
            model_name='user',
            name='modified',
        ),
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(verbose_name='last login', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=None, verbose_name='password', max_length=128),
            preserve_default=False,
        ),
    ]
