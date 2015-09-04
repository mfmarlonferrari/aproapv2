# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0014_auto_20150902_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='resultadoVotacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('totalDeVotosRecebidos', models.FloatField()),
                ('questao', models.ForeignKey(to='aproap.ideaDeQuestao')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
