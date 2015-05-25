# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentTableNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('table_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PostRanking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('ranking', models.IntegerField(db_index=True)),
                ('post', models.ForeignKey(to='posts.Post')),
            ],
        ),
        migrations.CreateModel(
            name='UserPostRanking1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('ranking', models.IntegerField(db_index=True)),
                ('post', models.ForeignKey(to='posts.Post')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPostRanking2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('ranking', models.IntegerField(db_index=True)),
                ('post', models.ForeignKey(to='posts.Post')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userpostranking2',
            unique_together=set([('user', 'post')]),
        ),
        migrations.AlterUniqueTogether(
            name='userpostranking1',
            unique_together=set([('user', 'post')]),
        ),
    ]
