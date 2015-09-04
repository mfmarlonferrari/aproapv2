# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0015_resultadovotacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultadovotacao',
            name='projeto',
            field=models.ForeignKey(default=1, to='aproap.Projeto'),
            preserve_default=False,
        ),
    ]
