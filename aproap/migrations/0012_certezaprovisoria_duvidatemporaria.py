# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0011_auto_20150901_1508'),
    ]

    operations = [
        migrations.CreateModel(
            name='certezaProvisoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usuario', models.CharField(max_length=100)),
                ('certeza', models.CharField(max_length=200)),
                ('qualProjeto', models.ForeignKey(to='aproap.Projeto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='duvidaTemporaria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usuario', models.CharField(max_length=100)),
                ('duvida', models.CharField(max_length=200)),
                ('qualProjeto', models.ForeignKey(to='aproap.Projeto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
