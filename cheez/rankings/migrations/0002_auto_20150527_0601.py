# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20150526_1422'),
        ('rankings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostRanking1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('ranking', models.IntegerField(db_index=True)),
                ('post', models.ForeignKey(to='posts.Post')),
            ],
        ),
        migrations.CreateModel(
            name='PostRanking2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('ranking', models.IntegerField(db_index=True)),
                ('post', models.ForeignKey(to='posts.Post')),
            ],
        ),
        migrations.RemoveField(
            model_name='postranking',
            name='post',
        ),
        migrations.DeleteModel(
            name='PostRanking',
        ),
    ]
