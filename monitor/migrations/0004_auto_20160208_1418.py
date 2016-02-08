# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20160208_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nic',
            name='nic_mask',
            field=models.CharField(default=b'None', max_length=64, verbose_name='\u5b50\u7f51\u63a9\u7801'),
        ),
    ]
