# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0006_mem_mem_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alarm_name', models.CharField(max_length=64, verbose_name='\u544a\u8b66\u540d\u79f0')),
                ('alarm_level', models.CharField(max_length=64, verbose_name='\u544a\u8b66\u7ea7\u522b')),
                ('alarm_detail', models.CharField(max_length=254, verbose_name='\u544a\u8b66\u63cf\u8ff0')),
                ('curr_datetime', models.FloatField(verbose_name='\u5f53\u524d\u65f6\u95f4\u6233')),
                ('host_name', models.ForeignKey(verbose_name='\u4e3b\u673a\u540d', to='monitor.Host')),
            ],
        ),
    ]
