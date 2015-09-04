# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ideadequestao',
            name='espaco',
            field=models.ForeignKey(default='1', to='aproap.espacoProjeto'),
            preserve_default=False,
        ),
    ]
