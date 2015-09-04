# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0006_auto_20150831_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='alunosnoprojeto',
            name='etapaAtual',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
