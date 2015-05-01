# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20150501_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likepost',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='like_posts'),
        ),
    ]
