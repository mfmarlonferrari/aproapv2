# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0013_alunosnoprojeto_ondeparou'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votosquestao',
            name='classificacao',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
