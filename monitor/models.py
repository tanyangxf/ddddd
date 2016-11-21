#coding:utf-8
from django.db import models
# Create your models here.
class Host(models.Model):
    host_name = models.CharField(max_length=64, verbose_name=u'主机名',unique=True)
    host_ip = models.GenericIPAddressField(verbose_name=u'IP地址',unique=True)
    host_ipmi = models.GenericIPAddressField(verbose_name=u'IPMI地址')
    def __unicode__(self):
        return self.host_name

#当前信息记录表
class Cpu(models.Model):
    host_name = models.ForeignKey('Host', verbose_name=u'主机名')
    l_cpu_count = models.IntegerField(verbose_name=u'逻辑CPU个数')
    cpu_percent = models.CharField(max_length=64,verbose_name=u'CPU使用总百分比')
    curr_datetime = models.FloatField(verbose_name=u'当前时间戳')

class Nic(models.Model):
    host_name = models.ForeignKey('Host', verbose_name=u'主机名')
    nic_name = models.CharField(max_length=64, verbose_name=u'网卡名')
    nic_ip = models.CharField(max_length=64,verbose_name=u'网卡IP地址')
    nic_mask = models.CharField(max_length=64,verbose_name=u'子网掩码',default='None')
    nic_sent = models.IntegerField(verbose_name=u'网卡发送大小')
    nic_recv = models.IntegerField(verbose_name=u'网卡接收大小')
    nic_speed = models.IntegerField(verbose_name=u'网卡速度')
    curr_datetime = models.FloatField(verbose_name=u'当前时间戳')

class Mem(models.Model):
    host_name = models.ForeignKey('Host', verbose_name=u'主机名') 
    mem_total = models.CharField(max_length=64,verbose_name=u'内存总量')
    mem_used = models.CharField(max_length=64, verbose_name=u'内存使用量')
    mem_percent = models.CharField(max_length=64,verbose_name=u'内存使用百分比')
    swap_total = models.CharField(max_length=64,verbose_name=u'swap总量')
    swap_used = models.CharField(max_length=64, verbose_name=u'swap使用量')
    swap_percent = models.CharField(max_length=64,verbose_name=u'swap使用百分比')
    curr_datetime = models.FloatField(verbose_name=u'当前时间戳')

class Disk(models.Model):
    host_name = models.ForeignKey('Host', verbose_name=u'主机名') 
    mountpoint_name = models.CharField(max_length=64, verbose_name=u'挂载点')
    disk_name = models.CharField(max_length=64, verbose_name=u'磁盘名称')
    disk_total = models.IntegerField(verbose_name=u'磁盘大小')
    disk_percent = models.FloatField(verbose_name=u'磁盘使用百分比') 
    curr_datetime = models.FloatField(verbose_name=u'当前时间戳')


class Alarm(models.Model):
    host_name = models.ForeignKey('Host', verbose_name=u'主机名') 
    alarm_name = models.CharField(max_length=64, verbose_name=u'告警名称')
    alarm_level = models.CharField(max_length=64, verbose_name=u'告警级别')
    alarm_detail = models.CharField(max_length=254,verbose_name=u'告警描述')
    curr_datetime = models.FloatField(verbose_name=u'当前时间戳')

#历史记录信息表
class Cpu_history(models.Model):
    host_name = models.ForeignKey('Host', verbose_name=u'主机名')
    l_cpu_count = models.IntegerField(verbose_name=u'逻辑CPU个数')
    cpu_percent = models.CharField(max_length=64,verbose_name=u'CPU使用总百分比')
    curr_datetime = models.FloatField(verbose_name=u'当前时间戳')

class Nic_history(models.Model):
    host_name = models.ForeignKey('Host', verbose_name=u'主机名')
    nic_name = models.CharField(max_length=64, verbose_name=u'网卡名')
    nic_ip = models.CharField(max_length=64,verbose_name=u'网卡IP地址')
    nic_mask = models.CharField(max_length=64,verbose_name=u'子网掩码',default='None')
    nic_sent = models.IntegerField(verbose_name=u'网卡发送大小')
    nic_recv = models.IntegerField(verbose_name=u'网卡接收大小')
    nic_speed = models.IntegerField(verbose_name=u'网卡速度')
    curr_datetime = models.FloatField(verbose_name=u'当前时间戳')

class Mem_history(models.Model):
    host_name = models.ForeignKey('Host', verbose_name=u'主机名') 
    mem_total = models.CharField(max_length=64, verbose_name=u'内存总量')
    mem_used = models.CharField(max_length=64, verbose_name=u'内存使用量')
    mem_percent = models.CharField(max_length=64, verbose_name=u'内存使用百分比')
    swap_total = models.CharField(max_length=64, verbose_name=u'swap总量')
    swap_used = models.CharField(max_length=64, verbose_name=u'swap使用量')
    swap_percent = models.CharField(max_length=64, verbose_name=u'swap使用百分比')
    curr_datetime = models.FloatField(verbose_name=u'当前时间戳')

class Disk_history(models.Model):
    host_name = models.ForeignKey('Host', verbose_name=u'主机名') 
    mountpoint_name = models.CharField(max_length=64, verbose_name=u'挂载点')
    disk_name = models.CharField(max_length=64, verbose_name=u'磁盘名称')
    disk_total = models.IntegerField(verbose_name=u'磁盘大小')
    disk_percent = models.FloatField(verbose_name=u'磁盘使用百分比') 
    curr_datetime = models.FloatField(verbose_name=u'当前时间戳')
