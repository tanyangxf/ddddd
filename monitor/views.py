#coding=utf-8
from django.shortcuts import render_to_response,HttpResponse
from monitor.models import Host, Mem, Nic, Disk
import json

# Create your views here.
def node_list(req):  
    #node_data:
    #[{'host_name': u'test'}, {'host_name': u'ty.lan'}]
    node_data = Host.objects.values('host_name').order_by('id')
    return render_to_response('monitor/node_list.html',{'node_data':node_data})

def node_monitor(req):
    try:
        #添加tabs之后url添加host_name参数发送过来
        host_name = req.GET['host_name']
        return render_to_response('monitor/node_monitor.html',{'host_name':host_name})
    except Exception:
        return HttpResponse('')

'''
def node_monitor(req):  
    #node_data:
    #[{'host_name': u'test'}, {'host_name': u'ty.lan'}]
    node_data = Host.objects.values('host_name')
    if req.method == 'POST':
        node_dict = {}
        host_name = req.POST['host_name']
        host_id = Host.objects.filter(host_name=host_name).values('id')[0].values()[0]
        host_ip = Host.objects.filter(host_name=host_name).values('host_ip')[0].values()
        host_disk = Disk.objects.filter(host_name_id=host_id).values()
            
        if host_disk:
            node_dict['disk_info'] = host_disk[0]
        else:
            node_dict['disk_info'] = ''
        node_dict['host_name'] = host_name
        node_dict['host_ip'] = host_ip
        node_dict = json.dumps(node_dict)
        return HttpResponse(node_dict)
   
    return render_to_response('monitor/node.html',{'node_data':node_data})
'''