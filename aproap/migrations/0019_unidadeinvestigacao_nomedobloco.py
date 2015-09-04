# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0018_unidadeinvestigacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='unidadeinvestigacao',
            name='nomeDoBloco',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
