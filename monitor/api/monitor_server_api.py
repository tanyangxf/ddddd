#coding:utf-8
from django.shortcuts import HttpResponse,render_to_response
from monitor.models import *
def collect(req):
    if req.method == 'POST':
        data = req.POST
        #return render_to_response('job/job_mgr.html',{'cpu_count':p_cpu_count})
        hostname = data.keys()[0].split('.')[0]
        #query result : ['{'id':1L}']
        host_id = Host.objects.values('id').filter(host_name=hostname)[0]['id']
        plugin_name = data.keys()[0].split('.')[1]
        monitor_data = eval(data.values()[0])
        if plugin_name == 'get_mem_info':
            mem_total = monitor_data['mem_total']
            mem_percent = monitor_data['mem_percent']
            swap_total = monitor_data['swap_total']
            swap_percent = monitor_data['swap_percent']
            data_insert = Mem(mem_total=mem_total,mem_percent=mem_percent,
                              swap_total=swap_total,swap_percent=swap_percent,host_name_id=host_id)  
            data_insert.save()
        elif plugin_name == 'get_cpu_info':
            l_cpu_count = monitor_data['l_cpu_count']
            cpu_percent = monitor_data['cpu_percent']
            data_insert = Cpu(l_cpu_count=l_cpu_count,cpu_percent=cpu_percent,host_name_id=host_id)
            data_insert.save()
        elif plugin_name == 'get_net_info':
            for nic_name in monitor_data.values():
                nic_dict = monitor_data[nic_name]
                nic_ip = nic_dict['nic_ip']
                nic_netmask = nic_dict['nic_netmask']
                nic_sent = nic_dict['nic_bytes_sent']/1024/1024
                nic_recv = nic_dict['nic_bytes_recv']/1024/1024
                nic_speed = nic_dict['nic_speed']
                data_insert = Nic(nic_name=nic_name,nic_ip=nic_ip,nic_netmask=nic_netmask,
                                  nic_sent=nic_sent,nic_recv=nic_recv,nic_speed=nic_speed,
                                  host_name_id=host_id)
                data_insert.save()
        elif plugin_name == 'get_disk_info':
            for mountpoint_name in monitor_data.values():
                disk_dict = monitor_data[mountpoint_name]
                disk_name = disk_dict['disk_name']
                disk_total = disk_dict['disk_total']
                disk_percent = disk_dict['disk_percent']
                data_insert = Disk(mountpoint_name=mountpoint_name,disk_name=disk_name,
                                   disk_total=disk_total,disk_percent,host_name_id=host_id)
                data_insert.save()
        else:
            return HttpResponse('failed')
        return HttpResponse('ok')
    else:
        return render_to_response('index.html')