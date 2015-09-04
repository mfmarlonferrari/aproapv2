# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0017_remove_resultadovotacao_projeto'),
    ]

    operations = [
        migrations.CreateModel(
            name='unidadeInvestigacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('conhecimentoPrevio', models.CharField(max_length=200)),
                ('qualProjeto', models.ForeignKey(to='aproap.Projeto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
