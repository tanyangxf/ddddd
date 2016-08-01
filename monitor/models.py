#coding:utf-8
from django.db import models

# Create your models here.
class Host(models.Model):
    host_name = models.CharField(max_length=64, verbose_name=u'主机名',unique=True)
    host_ip = models.GenericIPAddressField(verbose_name=u'IP地址',unique=True)
    host_ipmi = models.GenericIPAddressField(verbose_name=u'IPMI地址',unique=True)
    def __unicode__(self):
        return self.host_name

class Cpu(models.Model):
    host_name = models.ForeignKey('Host', verbose_name=u'主机名')
    l_cpu_count = models.IntegerField(verbose_name=u'逻辑CPU个数')
    cpu_percent = models.FloatField(verbose_name=u'CPU使用总百分比')

class Nic(models.Model):
    host_name = models.ForeignKey('Host', verbose_name=u'主机名')
    nic_name = models.CharField(max_length=64, verbose_name=u'网卡名')
    nic_ip = models.CharField(max_length=64,verbose_name=u'网卡IP地址')
    nic_mask = models.CharField(max_length=64,verbose_name=u'子网掩码',default='None')
    nic_sent = models.IntegerField(verbose_name=u'网卡发送大小')
    nic_recv = models.IntegerField(verbose_name=u'网卡接收大小')
    nic_speed = models.IntegerField(verbose_name=u'网卡速度')

class Mem(models.Model):
    host_name = models.ForeignKey('Host', verbose_name=u'主机名') 
    mem_total = models.IntegerField(verbose_name=u'内存总量')
    mem_percent = models.FloatField(verbose_name=u'内存使用百分比')
    swap_total = models.IntegerField(verbose_name=u'swap总量')
    swap_percent = models.FloatField(verbose_name=u'swap使用百分比')

class Disk(models.Model):
    host_name = models.ForeignKey('Host', verbose_name=u'主机名') 
    mountpoint_name = models.CharField(max_length=64, verbose_name=u'挂载点')
    disk_name = models.CharField(max_length=64, verbose_name=u'磁盘名称')
    disk_total = models.IntegerField(verbose_name=u'磁盘大小')
    disk_percent = models.FloatField(verbose_name=u'磁盘使用百分比') 
