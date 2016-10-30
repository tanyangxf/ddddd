# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysmgr', '0007_auto_20161029_1226'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
