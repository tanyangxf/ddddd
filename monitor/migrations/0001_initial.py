# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cpu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('l_cpu_count', models.IntegerField(verbose_name='\u903b\u8f91CPU\u4e2a\u6570')),
                ('cpu_percent', models.FloatField(verbose_name='CPU\u4f7f\u7528\u603b\u767e\u5206\u6bd4')),
            ],
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mountpoint_name', models.CharField(max_length=64, verbose_name='\u6302\u8f7d\u70b9')),
                ('disk_name', models.CharField(max_length=64, verbose_name='\u78c1\u76d8\u540d\u79f0')),
                ('disk_total', models.IntegerField(verbose_name='\u78c1\u76d8\u5927\u5c0f')),
                ('disk_percent', models.FloatField(verbose_name='\u78c1\u76d8\u4f7f\u7528\u767e\u5206\u6bd4')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host_name', models.CharField(max_length=64, verbose_name='\u4e3b\u673a\u540d')),
                ('ip_addr', models.GenericIPAddressField(verbose_name='IP\u5730\u5740')),
                ('ipmi_ip', models.GenericIPAddressField(verbose_name='IPMI\u5730\u5740')),
            ],
        ),
        migrations.CreateModel(
            name='Mem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mem_total', models.IntegerField(verbose_name='\u5185\u5b58\u603b\u91cf')),
                ('mem_percent', models.FloatField(verbose_name='\u5185\u5b58\u4f7f\u7528\u767e\u5206\u6bd4')),
                ('swap_total', models.IntegerField(verbose_name='swap\u603b\u91cf')),
                ('swap_percent', models.FloatField(verbose_name='swap\u4f7f\u7528\u767e\u5206\u6bd4')),
                ('host_name', models.ForeignKey(verbose_name='\u4e3b\u673a\u540d', to='monitor.Host')),
            ],
        ),
        migrations.CreateModel(
            name='Nic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nic_name', models.CharField(max_length=64, verbose_name='\u7f51\u5361\u540d')),
                ('nic_ip', models.GenericIPAddressField(verbose_name='\u7f51\u5361IP\u5730\u5740')),
                ('nic_mask', models.GenericIPAddressField(verbose_name='\u5b50\u7f51\u63a9\u7801')),
                ('nic_sent', models.IntegerField(verbose_name='\u7f51\u5361\u53d1\u9001\u5927\u5c0f')),
                ('nic_recv', models.IntegerField(verbose_name='\u7f51\u5361\u63a5\u6536\u5927\u5c0f')),
                ('nic_speed', models.IntegerField(verbose_name='\u7f51\u5361\u901f\u5ea6')),
                ('host_name', models.ForeignKey(verbose_name='\u4e3b\u673a\u540d', to='monitor.Host')),
            ],
        ),
        migrations.AddField(
            model_name='disk',
            name='host_name',
            field=models.ForeignKey(verbose_name='\u4e3b\u673a\u540d', to='monitor.Host'),
        ),
        migrations.AddField(
            model_name='cpu',
            name='host_name',
            field=models.ForeignKey(verbose_name='\u4e3b\u673a\u540d', to='monitor.Host'),
        ),
    ]
