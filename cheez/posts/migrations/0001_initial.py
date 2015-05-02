# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LikePostRel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('like_type', models.IntegerField(default=0, choices=[(-1, 'HATE'), (0, 'PASS'), (1, 'LIKE')])),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('like_count', models.IntegerField(default=0)),
                ('read_count', models.IntegerField(default=0)),
                ('source_url', models.URLField()),
                ('subtitle', models.CharField(null=True, max_length=512)),
                ('title', models.CharField(max_length=256)),
                ('like_users', models.ManyToManyField(related_name='like_posts', to=settings.AUTH_USER_MODEL, through='posts.LikePostRel')),
            ],
        ),
        migrations.CreateModel(
            name='ReadPostRel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(to='posts.Post')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='post',
            name='read_users',
            field=models.ManyToManyField(related_name='read_posts', to=settings.AUTH_USER_MODEL, through='posts.ReadPostRel'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(related_name='writed_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='likepostrel',
            name='post',
            field=models.ForeignKey(related_name='like_post_rels', to='posts.Post'),
        ),
        migrations.AddField(
            model_name='likepostrel',
            name='user',
            field=models.ForeignKey(related_name='like_post_rels', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='likepostrel',
            unique_together=set([('user', 'post')]),
        ),
    ]
