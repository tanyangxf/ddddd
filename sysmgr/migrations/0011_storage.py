# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysmgr', '0010_user_other_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('folder_name', models.CharField(unique=True, max_length=254, verbose_name='\u8bbe\u5907\u540d')),
                ('share_type', models.CharField(max_length=254, verbose_name='\u5171\u4eab\u7c7b\u578b')),
                ('share_parameter', models.CharField(max_length=254, verbose_name='\u5171\u4eab\u53c2\u6570')),
                ('allow_ip', models.CharField(max_length=254, verbose_name='\u5141\u8bb8\u8bbf\u95ee\u7684ip')),
                ('share_permission', models.CharField(max_length=254, verbose_name='\u5171\u4eab\u6743\u9650')),
                ('host_name', models.CharField(max_length=254, verbose_name='\u5171\u4eab\u4e3b\u673a')),
            ],
        ),
    ]
