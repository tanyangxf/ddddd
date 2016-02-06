#coding:utf-8
from django.db import models

# Create your models here.
class Job_list(models.Model):
    job_id = models.IntegerField(verbose_name=u'作业ID')
    job_name = models.CharField(max_length=40, verbose_name=u'作业名称')
    job_user_name = models.CharField(max_length=20, verbose_name=u'用户名')
    job_queue = models.CharField(max_length=20, verbose_name=u'队列')
    job_start_time = models.CharField(max_length=40,verbose_name=u'开始时间')
    job_run_time = models.CharField(max_length=40,verbose_name=u'运行时间')
    job_status = models.CharField(max_length=20,verbose_name=u'运行状态')