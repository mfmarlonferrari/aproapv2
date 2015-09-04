# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0010_auto_20150901_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votosquestao',
            name='questao',
            field=models.ForeignKey(to='aproap.ideaDeQuestao'),
            preserve_default=True,
        ),
    ]
