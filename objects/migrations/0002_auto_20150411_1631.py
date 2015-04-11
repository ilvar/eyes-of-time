# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='lat',
            field=models.DecimalField(default=0, max_digits=20, decimal_places=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='lon',
            field=models.DecimalField(default=0, max_digits=20, decimal_places=6),
            preserve_default=False,
        ),
    ]
