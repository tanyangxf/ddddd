# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysmgr', '0006_auto_20160731_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=8192, verbose_name=b'\xe5\xaf\x86\xe7\xa0\x81'),
        ),
    ]
