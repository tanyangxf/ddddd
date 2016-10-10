# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0004_auto_20161010_0205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mem',
            name='host_name',
        ),
        migrations.RemoveField(
            model_name='mem_history',
            name='host_name',
        ),
        migrations.DeleteModel(
            name='Mem',
        ),
        migrations.DeleteModel(
            name='Mem_history',
        ),
    ]
