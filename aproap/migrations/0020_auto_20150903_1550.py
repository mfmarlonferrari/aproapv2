# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aproap', '0019_unidadeinvestigacao_nomedobloco'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certezaprovisoria',
            old_name='certeza',
            new_name='texto',
        ),
        migrations.RenameField(
            model_name='duvidatemporaria',
            old_name='duvida',
            new_name='texto',
        ),
    ]
