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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(unique=True, max_length=126, null=True)),
                ('followee_count', models.IntegerField(blank=True, default=0)),
                ('follower_count', models.IntegerField(blank=True, default=0)),
                ('joined', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=128, null=True)),
                ('profile_image', models.ImageField(null=True, upload_to='images/users/profile', blank=True)),
                ('upload_count', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(verbose_name='groups', related_query_name='user', to='auth.Group', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True)),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', related_query_name='user', to='auth.Permission', related_name='user_set', help_text='Specific permissions for this user.', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('device_id', models.CharField(max_length=128)),
                ('os_type', models.IntegerField(choices=[(1, 'ANDROID'), (2, 'IOS')], default=1)),
                ('os_version', models.CharField(max_length=64, null=True)),
                ('push_token', models.CharField(max_length=256, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='devices', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SNSAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('sns_profile_url', models.URLField(null=True)),
                ('sns_type', models.IntegerField(choices=[(1, 'FACEBOOK')], default=1)),
                ('sns_user_id', models.CharField(max_length=128)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='sns_accounts', null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='snsaccount',
            unique_together=set([('sns_type', 'sns_user_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='device',
            unique_together=set([('os_type', 'device_id')]),
        ),
    ]
