#coding=utf-8
from django.shortcuts import render_to_response,HttpResponse
from monitor.models import Host, Mem, Nic, Disk,Cpu

# Create your views here.
def node_list(req):  
    req.session.set_expiry(1800)
    #node_data:
    #[{'host_name': u'test'}, {'host_name': u'ty.lan'}]
    node_data = Host.objects.values('host_name').order_by('id')
    return render_to_response('monitor/node_list.html',{'node_data':node_data})

def node_monitor(req):
    req.session.set_expiry(1800)
    try:
        #添加tabs之后url添加host_name参数发送过来
        host_name = req.GET['host_name']
        node_dict = {}
        host_id = Host.objects.filter(host_name=host_name).values('id')[0].values()[0]
        host_ip = Host.objects.filter(host_name=host_name).values('host_ip')[0].values()[0]
        '''
        [{'mem_percent': 65.8, 'swap_total': 2048L, u'host_name_id': 44L, 'swap_percent': 50.0,
         'mem_total': 8192L, u'id': 1L, 'curr_datetime': 1475918258.17232}]
        '''
        host_mem = Mem.objects.filter(host_name_id=host_id).values()
        '''
        [{u'host_name_id': 44L, 'curr_datetime': 1475918249.22358, 'l_cpu_count': 4L, u'id': 13L, 'cpu_percent': 7.5}]
        '''
        host_cpu = Cpu.objects.filter(host_name_id=host_id).values()
        '''
        {'disk_percent': 43.6, u'host_name_id': 44L, 'disk_total': 232L, 'curr_datetime': 1475916058.68999, 
        'mountpoint_name': u'/', u'id': 1L, 'disk_name': u'/dev/disk1'}
        '''
        host_disk = Disk.objects.filter(host_name_id=host_id).values()
        '''
        {'nic_name': u'en0', 'nic_ip': u'192.168.1.105', 'nic_sent': 1352L, u'host_name_id': 44L, 
        'nic_speed': 0L, 'nic_mask': u'255.255.255.0', 'nic_recv': 48707L, u'id': 1L, 'curr_datetime': 1475916664.5616}
        '''
        host_nic = Nic.objects.filter(host_name_id=host_id).values()
        #host_mem[0]['mem_total'] = host_mem[0]['mem_total'] + 'M'

        if host_mem:
            node_dict['host_mem'] = host_mem[0]
        if host_cpu:   
            node_dict['host_cpu'] = host_cpu[0]
        node_dict['host_nic'] = host_nic     
        node_dict['host_disk'] = host_disk      
        node_dict['host_name'] = host_name
        node_dict['host_ip'] = host_ip
        return render_to_response('monitor/node_monitor.html',node_dict)
    except Exception:
        return HttpResponse('')
