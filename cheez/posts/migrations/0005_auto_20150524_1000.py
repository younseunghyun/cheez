# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20150524_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='posts', to='posts.Tag'),
        ),
    ]
