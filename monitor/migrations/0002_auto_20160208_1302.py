# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='host_name',
            field=models.CharField(unique=True, max_length=64, verbose_name='\u4e3b\u673a\u540d'),
        ),
    ]
