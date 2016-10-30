# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysmgr', '0008_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(unique=True, max_length=254, verbose_name='\u7528\u6237\u540d')),
                ('password', models.CharField(max_length=254, verbose_name='\u7528\u6237\u5bc6\u7801')),
                ('userid', models.IntegerField(unique=True, verbose_name='\u7528\u6237ID')),
                ('user_group', models.CharField(max_length=254, verbose_name='\u7528\u6237\u7ec4')),
                ('user_home', models.CharField(max_length=254, verbose_name='\u7528\u6237\u4e3b\u76ee\u5f55')),
                ('user_type', models.CharField(max_length=20, verbose_name='\u7528\u6237\u7c7b\u578b')),
                ('user_mail', models.CharField(max_length=50, verbose_name='\u7528\u6237\u90ae\u4ef6')),
                ('user_tel', models.CharField(max_length=30, verbose_name='\u7528\u6237\u7535\u8bdd')),
                ('user_comment', models.CharField(max_length=254, verbose_name='\u7528\u6237\u63cf\u8ff0')),
                ('is_login', models.CharField(default=b'True', max_length=10, verbose_name='\u662f\u5426\u80fd\u767b\u5f55')),
            ],
        ),
    ]
