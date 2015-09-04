# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0003_auto_20150831_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projeto',
            name='dataPublicacao',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]
