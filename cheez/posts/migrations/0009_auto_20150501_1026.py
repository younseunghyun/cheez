# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0008_readpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='readpost',
            name='post',
            field=models.ForeignKey(to='posts.Post', default=None, related_name='read_posts'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='readpost',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=None, related_name='read_posts'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='likepost',
            name='post',
            field=models.ForeignKey(related_name='like_posts', to='posts.Post'),
        ),
        migrations.AlterField(
            model_name='likepost',
            name='user',
            field=models.ForeignKey(to_field='like_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
