# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysmgr', '0009_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='other_group',
            field=models.CharField(default='', max_length=254, verbose_name='\u9644\u52a0\u7ec4'),
            preserve_default=False,
        ),
    ]
