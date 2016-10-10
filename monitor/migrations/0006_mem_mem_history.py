# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0005_auto_20161010_0551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mem_total', models.CharField(max_length=64, verbose_name='\u5185\u5b58\u603b\u91cf')),
                ('mem_used', models.CharField(max_length=64, verbose_name='\u5185\u5b58\u4f7f\u7528\u91cf')),
                ('mem_percent', models.CharField(max_length=64, verbose_name='\u5185\u5b58\u4f7f\u7528\u767e\u5206\u6bd4')),
                ('swap_total', models.CharField(max_length=64, verbose_name='swap\u603b\u91cf')),
                ('swap_used', models.CharField(max_length=64, verbose_name='swap\u4f7f\u7528\u91cf')),
                ('swap_percent', models.CharField(max_length=64, verbose_name='swap\u4f7f\u7528\u767e\u5206\u6bd4')),
                ('curr_datetime', models.FloatField(verbose_name='\u5f53\u524d\u65f6\u95f4\u6233')),
                ('host_name', models.ForeignKey(verbose_name='\u4e3b\u673a\u540d', to='monitor.Host')),
            ],
        ),
        migrations.CreateModel(
            name='Mem_history',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mem_total', models.CharField(max_length=64, verbose_name='\u5185\u5b58\u603b\u91cf')),
                ('mem_used', models.CharField(max_length=64, verbose_name='\u5185\u5b58\u4f7f\u7528\u91cf')),
                ('mem_percent', models.CharField(max_length=64, verbose_name='\u5185\u5b58\u4f7f\u7528\u767e\u5206\u6bd4')),
                ('swap_total', models.CharField(max_length=64, verbose_name='swap\u603b\u91cf')),
                ('swap_used', models.CharField(max_length=64, verbose_name='swap\u4f7f\u7528\u91cf')),
                ('swap_percent', models.CharField(max_length=64, verbose_name='swap\u4f7f\u7528\u767e\u5206\u6bd4')),
                ('curr_datetime', models.FloatField(verbose_name='\u5f53\u524d\u65f6\u95f4\u6233')),
                ('host_name', models.ForeignKey(verbose_name='\u4e3b\u673a\u540d', to='monitor.Host')),
            ],
        ),
    ]
