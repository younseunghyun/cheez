# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ogp', '0002_auto_20150505_1406'),
    ]

    operations = [
        migrations.RenameField(
            model_name='og',
            old_name='image_url',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='og',
            old_name='video_url',
            new_name='video',
        ),
    ]
