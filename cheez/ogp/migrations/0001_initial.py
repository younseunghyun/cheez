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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('url', models.URLField()),
                ('title', models.CharField(null=True, max_length=1024)),
                ('author', models.CharField(null=True, max_length=256)),
                ('image', models.URLField(null=True)),
                ('video', models.URLField(null=True)),
                ('description', models.CharField(null=True, max_length=2048)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
