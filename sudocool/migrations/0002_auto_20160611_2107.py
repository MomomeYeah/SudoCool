# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sudocool', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sudocoolboard',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
