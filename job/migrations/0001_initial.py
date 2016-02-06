# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job_list',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_id', models.IntegerField(verbose_name='\u4f5c\u4e1aID')),
                ('job_name', models.CharField(max_length=20, verbose_name='\u4f5c\u4e1a\u540d\u79f0')),
                ('job_user_name', models.CharField(max_length=20, verbose_name='\u7528\u6237\u540d')),
                ('job_queue', models.CharField(max_length=20, verbose_name='\u961f\u5217')),
                ('job_start_time', models.DateTimeField(verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('job_run_time', models.DateTimeField(verbose_name='\u8fd0\u884c\u65f6\u95f4')),
                ('job_status', models.CharField(max_length=20, verbose_name='\u8fd0\u884c\u72b6\u6001')),
            ],
        ),
    ]
