# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0002_auto_20150411_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='img',
            field=models.ImageField(upload_to=b'', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='lat',
            field=models.DecimalField(max_digits=20, decimal_places=16),
        ),
        migrations.AlterField(
            model_name='event',
            name='lon',
            field=models.DecimalField(max_digits=20, decimal_places=16),
        ),
    ]
