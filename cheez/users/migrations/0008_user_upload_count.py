# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20150522_0639'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='upload_count',
            field=models.IntegerField(default=0),
        ),
    ]
