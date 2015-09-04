# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0005_auto_20150831_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alunosnoprojeto',
            name='projeto',
            field=models.ForeignKey(to='aproap.Projeto'),
            preserve_default=True,
        ),
    ]
