# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0006_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='ip_addr',
            field=models.GenericIPAddressField(unique=True, verbose_name='IP\u5730\u5740'),
        ),
        migrations.AlterField(
            model_name='host',
            name='ipmi_ip',
            field=models.GenericIPAddressField(unique=True, verbose_name='IPMI\u5730\u5740'),
        ),
    ]
