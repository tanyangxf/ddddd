# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0008_auto_20160801_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='host_ipmi',
            field=models.GenericIPAddressField(verbose_name='IPMI\u5730\u5740'),
        ),
    ]
