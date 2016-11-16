# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysmgr', '0011_storage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storage',
            old_name='host_name',
            new_name='share_host',
        ),
    ]
