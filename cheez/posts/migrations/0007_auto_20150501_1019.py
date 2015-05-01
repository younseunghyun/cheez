# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20150501_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='read_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='likepost',
            name='post',
            field=models.ForeignKey(to='posts.Post', related_name='likes'),
        ),
    ]
