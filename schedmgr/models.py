#coding:utf-8
from django.db import models

# Create your models here.
class Queue_list(models.Model):
    queue_name = models.CharField(max_length=40, verbose_name=u'队列名称')

class Sched_service_list(models.Model):
    service_name = models.CharField(max_length=40, verbose_name=u'服务名称')
    service_type = models.CharField(max_length=10, verbose_name=u'服务类型')
    service_home = models.CharField(max_length=255, verbose_name=u'服务主目录')
    service_process = models.CharField(max_length=255, verbose_name=u'服务进程')