# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0005_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
