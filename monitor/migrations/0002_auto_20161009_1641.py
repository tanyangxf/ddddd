# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mem',
            name='mem_percent',
            field=models.CharField(max_length=64, verbose_name='\u5185\u5b58\u4f7f\u7528\u767e\u5206\u6bd4'),
        ),
        migrations.AlterField(
            model_name='mem',
            name='mem_total',
            field=models.CharField(max_length=64, verbose_name='\u5185\u5b58\u603b\u91cf'),
        ),
        migrations.AlterField(
            model_name='mem',
            name='swap_percent',
            field=models.CharField(max_length=64, verbose_name='swap\u4f7f\u7528\u767e\u5206\u6bd4'),
        ),
        migrations.AlterField(
            model_name='mem',
            name='swap_total',
            field=models.CharField(max_length=64, verbose_name='swap\u603b\u91cf'),
        ),
    ]
