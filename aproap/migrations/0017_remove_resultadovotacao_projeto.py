# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0016_resultadovotacao_projeto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultadovotacao',
            name='projeto',
        ),
    ]
