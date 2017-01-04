#coding:utf-8
from django.db import models

# Create your models here.
class Queue_list(models.Model):
    queue_name = models.CharField(max_length=40, verbose_name=u'队列名称')
