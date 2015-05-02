# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(null=True, max_length=256, unique=True)),
                ('name', models.CharField(null=True, max_length=128)),
                ('groups', models.ManyToManyField(verbose_name='groups', to='auth.Group', related_name='user_set', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True)),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', to='auth.Permission', related_name='user_set', related_query_name='user', help_text='Specific permissions for this user.', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('device_id', models.CharField(max_length=512, unique=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='devices')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SNSAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('sns_profile_url', models.URLField(null=True)),
                ('sns_type', models.IntegerField(default=1, choices=[(1, 'FACEBOOK')])),
                ('sns_user_id', models.CharField(max_length=128)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='sns_accounts')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='snsaccount',
            unique_together=set([('sns_type', 'sns_user_id')]),
        ),
    ]
