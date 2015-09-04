# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0008_myobject'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyObject',
        ),
        migrations.AlterField(
            model_name='votosquestao',
            name='usuario',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
