# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_tag_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='post_count',
            field=models.IntegerField(default=1),
        ),
    ]
