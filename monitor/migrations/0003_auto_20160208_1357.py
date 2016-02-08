# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_auto_20160208_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nic',
            name='nic_ip',
            field=models.CharField(max_length=64, verbose_name='\u7f51\u5361IP\u5730\u5740'),
        ),
        migrations.AlterField(
            model_name='nic',
            name='nic_mask',
            field=models.CharField(max_length=64, verbose_name='\u5b50\u7f51\u63a9\u7801'),
        ),
    ]
