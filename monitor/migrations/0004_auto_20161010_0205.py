# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20161009_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cpu',
            name='cpu_percent',
            field=models.CharField(max_length=64, verbose_name='CPU\u4f7f\u7528\u603b\u767e\u5206\u6bd4'),
        ),
        migrations.AlterField(
            model_name='cpu_history',
            name='cpu_percent',
            field=models.CharField(max_length=64, verbose_name='CPU\u4f7f\u7528\u603b\u767e\u5206\u6bd4'),
        ),
    ]
