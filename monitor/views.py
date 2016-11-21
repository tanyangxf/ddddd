#coding=utf-8
from django.shortcuts import HttpResponse,redirect,render
from monitor.models import Host, Mem, Nic, Disk,Cpu, Alarm
import csv
import time
import json
# Create your views here.
def node_list(req):  
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    #node_data:
    #[{'host_name': u'test'}, {'host_name': u'ty.lan'}]
    node_data = Host.objects.values('host_name').order_by('id')
    return render(req,'monitor/node_list.html',{'node_data':node_data})

def node_monitor(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
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
        return render(req,'monitor/node_monitor.html',node_dict)
    except Exception:
        return HttpResponse('')
    
def report_monitor_index(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login") 
    return render(req,'monitor/report_monitor_index.html')

def report_monitor_cpu(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login") 
    #生成csv文件
    response = HttpResponse(content_type='text/csv')
    curr_time = time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime())
    response['Content-Disposition'] = 'attachment; filename="report_monitor_cpu_%s.csv"'%curr_time
    writer = csv.writer(response)
    report_head = [u'主机名',u'CPU个数',u'CPU使用率',u'时间']
    writer.writerow([unicode(s).encode("gb2312") for s in report_head])
    all_result = Host.objects.raw('select a.id,a.host_name,b.l_cpu_count,b.cpu_percent,b.curr_datetime from monitor_host a,\
                                    monitor_cpu_history b where a.id=b.host_name_id order by a.host_name,b.curr_datetime desc')
    for i in all_result:
        result_list = []
        result_list.append(i.host_name)
        result_list.append(i.l_cpu_count)
        result_list.append(i.cpu_percent)
        c_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i.curr_datetime))
        result_list.append(c_time)
        writer.writerow(result_list)
    return response

def report_monitor_mem(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login") 
    #生成csv文件
    response = HttpResponse(content_type='text/csv')
    curr_time = time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime())
    response['Content-Disposition'] = 'attachment; filename="report_monitor_mem_%s.csv"'%curr_time
    writer = csv.writer(response)
    report_head = [u'主机名',u'内存大小',u'内存使用大小',u'内存使用率',u'SWAP大小',u'SWAP使用率',u'时间']
    writer.writerow([unicode(s).encode("gb2312") for s in report_head])
    all_result = Host.objects.raw('select a.id,a.host_name,b.mem_total,b.mem_used,b.mem_percent,b.swap_total,b.swap_percent,\
                                    b.curr_datetime from monitor_host a,monitor_mem_history b where a.id=b.host_name_id \
                                    order by a.host_name,b.curr_datetime desc;')
    for i in all_result:
        result_list = []
        result_list.append(i.host_name)
        result_list.append(i.mem_total)
        result_list.append(i.mem_used)
        result_list.append(i.mem_percent)
        result_list.append(i.swap_total)
        result_list.append(i.swap_percent)
        c_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i.curr_datetime))
        result_list.append(c_time)
        writer.writerow(result_list)
    return response

def report_monitor_net(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login") 
    #生成csv文件
    response = HttpResponse(content_type='text/csv')
    curr_time = time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime())
    response['Content-Disposition'] = 'attachment; filename="report_monitor_net_%s.csv"'%curr_time
    writer = csv.writer(response)
    report_head = [u'主机名',u'网卡名称',u'网卡IP地址',u'发送包大小',u'接收包大小',u'时间']
    writer.writerow([unicode(s).encode("gb2312") for s in report_head])
    all_result = Host.objects.raw('select a.id,a.host_name,b.nic_name,b.nic_ip,b.nic_sent,b.nic_recv,b.curr_datetime \
                                    from monitor_host a,monitor_nic_history b where a.id=b.host_name_id \
                                    order by a.host_name,b.curr_datetime desc;')
    for i in all_result:
        result_list = []
        result_list.append(i.host_name)
        result_list.append(i.nic_name)
        result_list.append(i.nic_ip)
        result_list.append(i.nic_sent)
        result_list.append(i.nic_recv)
        c_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i.curr_datetime))
        result_list.append(c_time)
        writer.writerow(result_list)
    return response

def report_monitor_disk(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login") 
    #生成csv文件
    response = HttpResponse(content_type='text/csv')
    curr_time = time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime())
    response['Content-Disposition'] = 'attachment; filename="report_monitor_disk_%s.csv"'%curr_time
    writer = csv.writer(response)
    report_head = [u'主机名',u'挂载点',u'磁盘名称',u'磁盘总量',u'磁盘使用率',u'时间']
    writer.writerow([unicode(s).encode("gb2312") for s in report_head])
    all_result = Host.objects.raw('select a.id,a.host_name,b.mountpoint_name,b.disk_name,b.disk_total,b.disk_percent,b.curr_datetime \
                                    from monitor_host a,monitor_disk_history b order by a.host_name,b.curr_datetime desc;')
    for i in all_result:
        result_list = []
        result_list.append(i.host_name)
        result_list.append(i.mountpoint_name)
        result_list.append(i.disk_name)
        result_list.append(i.disk_total)
        result_list.append(i.disk_percent)
        c_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i.curr_datetime))
        result_list.append(c_time)
        writer.writerow(result_list)
    return response

def monitor_alarm_index(req,page):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login") 
    try:
        page = int(page)
    except Exception:
        page = 1
    num = 12
    start = (page - 1)*num
    end = page*12
    total = Alarm.objects.all().count()
    all_result = Host.objects.raw('select a.id,a.host_name,b.alarm_name,b.alarm_level,b.alarm_detail,b.curr_datetime from \
                                 monitor_host a,monitor_alarm b where a.id=b.host_name_id order by a.host_name,b.curr_datetime desc;')[start:end]
    #divmod(14,5),result 2,4
    temp = divmod(total,num)
    if temp[1] == 0:
        all_page_count = temp[0]
    else:
        all_page_count = temp[0] + 1
    
    all_result_list = []
    for i in all_result:
        result_list = {}
        result_list['host_name'] = i.host_name
        result_list['alarm_name'] = i.alarm_name
        result_list['alarm_level'] = i.alarm_level
        result_list['alarm_detail'] = i.alarm_detail
        result_list['id'] = i.id
        c_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i.curr_datetime))
        result_list['c_time'] = c_time
        all_result_list.append(result_list)
    return render(req,'monitor/monitor_alarm_index.html',{'alarm_data':all_result_list,'all_page_count':range(all_page_count)})

def del_alarm(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if req.method == 'POST':
        c_time = req.POST.get('c_time', None)
        if c_time:
            for i in c_time.split(','):
                c_time_format = time.strptime(i, "%Y-%m-%d %H:%M:%S");
                curr_datetime = int(time.mktime(c_time_format))
                del_data = Alarm.objects.get(curr_datetime__startswith=curr_datetime)
                del_data.delete()
        return HttpResponse('ok')
    if not user_dict:
        return redirect("/login") 
    return HttpResponse('no data')