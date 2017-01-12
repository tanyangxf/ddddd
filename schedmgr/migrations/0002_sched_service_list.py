# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedmgr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sched_service_list',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service_name', models.CharField(max_length=40, verbose_name='\u670d\u52a1\u540d\u79f0')),
                ('service_type', models.CharField(max_length=10, verbose_name='\u670d\u52a1\u7c7b\u578b')),
                ('service_home', models.CharField(max_length=255, verbose_name='\u670d\u52a1\u4e3b\u76ee\u5f55')),
                ('service_process', models.CharField(max_length=255, verbose_name='\u670d\u52a1\u8fdb\u7a0b')),
            ],
        ),
    ]
