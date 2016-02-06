# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job_list',
            name='job_run_time',
            field=models.CharField(max_length=20, verbose_name='\u8fd0\u884c\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='job_list',
            name='job_start_time',
            field=models.CharField(max_length=20, verbose_name='\u5f00\u59cb\u65f6\u95f4'),
        ),
    ]
