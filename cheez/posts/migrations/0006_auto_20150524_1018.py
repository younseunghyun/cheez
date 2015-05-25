# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0005_auto_20150524_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('reason', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='post',
            name='reported_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='post',
            field=models.ForeignKey(to='posts.Post'),
        ),
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
