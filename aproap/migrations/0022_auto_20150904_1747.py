# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0021_auto_20150904_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='conhecimento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usuario', models.CharField(max_length=100)),
                ('texto', models.CharField(max_length=200)),
                ('certezaOuDuvida', models.BooleanField()),
                ('qualProjeto', models.ForeignKey(to='aproap.Projeto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='conhecimentoprevio',
            name='qualProjeto',
        ),
        migrations.DeleteModel(
            name='conhecimentoPrevio',
        ),
    ]
