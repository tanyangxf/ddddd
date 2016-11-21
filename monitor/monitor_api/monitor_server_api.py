#coding:utf-8
from django.shortcuts import HttpResponse,redirect, render_to_response,render
from monitor.models import *
from django.template.context import RequestContext

import time
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def monitor_collect(req):
    if req.method == 'POST':
        data = req.POST
        #return render_to_response('job/job_mgr.html',{'cpu_count':p_cpu_count})
        host_name = data.keys()[0].split('#')[0]
        #query result : ['{'id':1L}']
        try:
            host_id = Host.objects.values('id').filter(host_name=host_name)[0]['id']
        except Exception,e:
            print 'Host is not found,please check monitor server config!'
            return HttpResponse('Host is not found,please check monitor server config!')
        plugin_name = data.keys()[0].split('#')[-1]
        monitor_data = eval(data.values()[0])
        if plugin_name == 'get_mem_info':
            mem_total = monitor_data['mem_total']
            mem_used = monitor_data['mem_used']
            mem_percent = monitor_data['mem_percent']
            swap_total = monitor_data['swap_total']
            swap_used = monitor_data['swap_used']
            swap_percent = monitor_data['swap_percent']
            curr_datetime = time.time()
            alarm_name = u'内存'
            #判断告警
            if swap_percent > 5 and swap_percent < 10:
                alarm_level = 'Warning'
                alarm_detail = u'内存使用过高'
                alarm_insert = Alarm(host_name_id=host_id,alarm_name=alarm_name,alarm_level=alarm_level,\
                                     alarm_detail=alarm_detail,curr_datetime=curr_datetime)
                alarm_insert.save()
            elif swap_percent > 10:
                print type(swap_percent)
                alarm_level = 'Critical'
                alarm_detail = u'内存严重不足'
                alarm_insert = Alarm(host_name_id=host_id,alarm_name=alarm_name,alarm_level=alarm_level,\
                                     alarm_detail=alarm_detail,curr_datetime=curr_datetime)
                alarm_insert.save()
            #插入历史记录表
            history_data_insert = Mem_history(mem_total=mem_total,mem_used=mem_used,mem_percent=mem_percent,
                              swap_total=swap_total,swap_used=swap_used,swap_percent=swap_percent,host_name_id=host_id,curr_datetime=curr_datetime) 
            history_data_insert.save()           
            #更新当前数据，先删除后插入
            curr_data_delete = Mem.objects.filter(host_name_id=host_id).delete()
            curr_data_insert = Mem(mem_total=mem_total,mem_used=mem_used,mem_percent=mem_percent,
                              swap_total=swap_total,swap_used=swap_used,swap_percent=swap_percent,host_name_id=host_id,curr_datetime=curr_datetime)
            curr_data_insert.save()
        elif plugin_name == 'get_cpu_info':
            l_cpu_count = int(monitor_data['l_cpu_count'])
            cpu_percent = monitor_data['cpu_percent']
            curr_datetime = time.time()
            alarm_name = u'cpu'
            #判断告警
            if cpu_percent > 80 and cpu_percent < 95:
                alarm_level = 'Warning'
                alarm_detail = u'cpu使用过高'
                alarm_insert = Alarm(host_name_id=host_id,alarm_name=alarm_name,alarm_level=alarm_level,
                                     alarm_detail=alarm_detail,curr_datetime=curr_datetime)
                alarm_insert.save()
            elif cpu_percent > 95:
                alarm_level = 'Critical'
                alarm_detail = u'cpu严重不足'
                alarm_insert = Alarm(host_name_id=host_id,alarm_name=alarm_name,alarm_level=alarm_level,
                                     alarm_detail=alarm_detail,curr_datetime=curr_datetime)
                alarm_insert.save()
            history_data_insert = Cpu_history(l_cpu_count=l_cpu_count,cpu_percent=cpu_percent,host_name_id=host_id,curr_datetime=curr_datetime)
            history_data_insert.save()
            curr_data_delete = Cpu.objects.filter(host_name_id=host_id).delete()
            curr_data_insert = Cpu(l_cpu_count=l_cpu_count,cpu_percent=cpu_percent,host_name_id=host_id,curr_datetime=curr_datetime)
            curr_data_insert.save()
        elif plugin_name == 'get_net_info':
            curr_data_delete = Nic.objects.filter(host_name_id=host_id).delete()
            for nic_name in monitor_data.keys():
                nic_dict = monitor_data[nic_name]
                nic_ip = str(nic_dict['nic_ip'])
                #mask may be is none
                nic_mask = str(nic_dict['nic_mask'])
                nic_sent = int(nic_dict['nic_bytes_sent']/1024/1024)
                nic_recv = int(nic_dict['nic_bytes_recv']/1024/1024)
                nic_speed = int(nic_dict['nic_speed'])
                curr_datetime = time.time()
                history_data_insert = Nic_history(nic_name=nic_name,nic_ip=nic_ip,nic_mask=nic_mask,
                                  nic_sent=nic_sent,nic_recv=nic_recv,nic_speed=nic_speed,
                                  host_name_id=host_id,curr_datetime=curr_datetime)
                history_data_insert.save()
                curr_data_insert = Nic(nic_name=nic_name,nic_ip=nic_ip,nic_mask=nic_mask,
                                  nic_sent=nic_sent,nic_recv=nic_recv,nic_speed=nic_speed,
                                  host_name_id=host_id,curr_datetime=curr_datetime)
                curr_data_insert.save()
        elif plugin_name == 'get_disk_info':
            curr_data_delete = Disk.objects.filter(host_name_id=host_id).delete()
            for mountpoint_name in monitor_data.keys():
                disk_dict = monitor_data[mountpoint_name]
                disk_name = str(disk_dict['disk_name'])
                disk_total = int(disk_dict['disk_total'])
                disk_percent = float(disk_dict['disk_percent'])
                curr_datetime = time.time()
                alarm_name = disk_name
                #判断告警
                if disk_percent > 80 and disk_percent < 95:
                    alarm_level = 'Warning'
                    alarm_detail = u'磁盘使用过高'
                    alarm_insert = Alarm(host_name_id=host_id,alarm_name=alarm_name,alarm_level=alarm_level,
                                         alarm_detail=alarm_detail,curr_datetime=curr_datetime)
                    alarm_insert.save()
                elif disk_percent > 95:
                    alarm_level = 'Critical'
                    alarm_detail = u'磁盘严重不足'
                    alarm_insert = Alarm(host_name_id=host_id,alarm_name=alarm_name,alarm_level=alarm_level,
                                         alarm_detail=alarm_detail,curr_datetime=curr_datetime)
                    alarm_insert.save()
                history_data_insert = Disk_history(mountpoint_name=mountpoint_name,disk_name=disk_name,
                                        disk_total=disk_total,disk_percent=disk_percent,host_name_id=host_id,curr_datetime=curr_datetime)
                history_data_insert.save()
                curr_data_insert = Disk(mountpoint_name=mountpoint_name,disk_name=disk_name,
                                   disk_total=disk_total,disk_percent=disk_percent,host_name_id=host_id,curr_datetime=curr_datetime)
                curr_data_insert.save()             
        else:
            return HttpResponse('failed')
        return HttpResponse('Monitor data update success!')
    else:
        return HttpResponse('no data!')