# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0009_auto_20150831_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votosquestao',
            name='questao',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
