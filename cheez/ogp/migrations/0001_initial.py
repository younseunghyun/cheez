# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OG',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('url', models.URLField(unique=True)),
                ('title', models.CharField(max_length=1024, null=True)),
                ('author', models.CharField(max_length=256)),
                ('image_url', models.URLField(null=True)),
                ('video_url', models.URLField(null=True)),
                ('description', models.CharField(max_length=2048, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
