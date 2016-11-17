# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysmgr', '0012_auto_20161115_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storage',
            name='folder_name',
            field=models.CharField(max_length=254, verbose_name='\u8bbe\u5907\u540d'),
        ),
    ]
