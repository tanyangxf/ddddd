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
    total = Host.objects.all().count()  
    return render(req,'monitor/node_list.html',{'node_data':node_data,'total':total})

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

def monitor_alarm_index(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login") 
    return render(req,'monitor/monitor_alarm_index.html')

def get_monitor_alarm(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login") 
    result_list = []
    alarm_list_info = {}
    if req.method == 'POST':
        try:
            search_host_name = req.POST.get('host_name', None)
            search_date_from = req.POST.get('date_from', None)
            search_date_to   = req.POST.get('date_to', None)
            search_sql = ''
            #排序,默认从id来排序
            sort_name = req.POST.get('sort','id')
            sort_order = req.POST.get('order','desc')
            #rows 每页显示多少条 
            #数据格式{'total':xx,'rows':[{r1:r1},{r2:r2}]}
            pageSize = int(req.POST.get('rows'))
            page = int(req.POST.get('page'))
            start = (page - 1)*pageSize
            #end = page*pageSize
            end = pageSize
            total = Alarm.objects.all().count()
            if search_host_name:
                search_sql = "a.host_name like '%%%%%s%%%%' and " %(search_host_name)
            if search_date_from:
                search_sql = "%s b.curr_datetime >= '%s' and " %(search_sql,search_date_from)
            if search_date_to:
                search_sql = "%s b.curr_datetime <= '%s' and " %(search_sql,search_date_to)
            if not search_sql:
                    search_sql = 'where '
            else:
                search_sql = 'where %s '%search_sql
            temp_result = Host.objects.raw("select b.id,a.id as host_id,a.host_name,b.alarm_name,b.alarm_level,b.alarm_detail,b.curr_datetime from \
                                         monitor_host a,monitor_alarm b   %s a.id=b.host_name_id order by %s,b.curr_datetime %s limit %s,%s;"%(search_sql,sort_name,sort_order,start,end))
            for i in temp_result:
                temp_list = {}
                temp_list['host_name'] = i.host_name
                temp_list['alarm_name'] = i.alarm_name
                temp_list['alarm_level'] = i.alarm_level
                temp_list['alarm_detail'] = i.alarm_detail
                temp_list['host_id'] = i.host_id
                temp_list['id'] = i.id
                c_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i.curr_datetime))
                temp_list['c_time'] = c_time
                result_list.append(temp_list)
            alarm_list_info['total'] = total
            alarm_list_info['rows'] = result_list
            alarm_list_info = json.dumps(alarm_list_info)
            return HttpResponse(alarm_list_info)
        except Exception,e:
            return HttpResponse(e)
    else:
        return HttpResponse(u'非法操作')



def del_alarm(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    if req.method == 'POST':
        alarm_ids = req.POST.get('alarm_id', None)
        if alarm_ids:
            for alarm_id in alarm_ids.split(','):
                del_data = Alarm.objects.filter(id=alarm_id)
                del_data.delete()
        return HttpResponse('ok')
    else:
        return HttpResponse(u'非法操作')
