# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name=b'SudocoolBoard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'created_date', models.DateTimeField()),
                (b'sudocoolData', models.CharField(max_length=161)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
