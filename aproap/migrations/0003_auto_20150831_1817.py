# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0002_ideadequestao_espaco'),
    ]

    operations = [
        migrations.CreateModel(
            name='alunosNoProjeto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aluno', models.CharField(max_length=100)),
                ('projeto', models.ForeignKey(to='aproap.Projeto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='questaoInvestigacao',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
