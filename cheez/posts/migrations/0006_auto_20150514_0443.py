# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_tag_post_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='post_count',
            field=models.IntegerField(default=0),
        ),
    ]
