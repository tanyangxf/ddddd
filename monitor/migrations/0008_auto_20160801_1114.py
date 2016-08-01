# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0007_auto_20160731_2044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host',
            old_name='ip_addr',
            new_name='host_ip',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='ipmi_ip',
            new_name='host_ipmi',
        ),
    ]
