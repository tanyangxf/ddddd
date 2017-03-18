#coding:utf-8
from django.shortcuts import render,HttpResponse, redirect
import commands
from monitor.models import Host,Mem
from string import lower
import json
from sysmgr.models import User
from config.config import * 
from models import Queue_list
import os
from schedmgr.models import Sched_service_list
from clusmgr.remote_help import exec_commands,connect
# Create your views here.

def queue_tree(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    return render(req,'schedmgr/queue_tree.html')

#{'high':{"max_job":0,"run_job":0,default_queue:'true'},'low':}
def mgr_queue_index(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse(u'非法操作')
    return render(req,'schedmgr/mgr_queue.html')

    
def get_queue_list(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse(u'非法操作')
    if req.method == 'POST':
        pbs_server_status = commands.getstatusoutput(QMGR + ' -c "list server"')
        if pbs_server_status[0]:
            return HttpResponse('failed')
        cmd = commands.getstatusoutput(QSTAT +' -Q')
        if not cmd[0]:
            try:
                default_queue = commands.getoutput(QMGR + ' -c "list server default"|grep default_queue')
                default_queue_name = default_queue.split('=')[1].strip()
                queue_temp_list = cmd[1].split('\n')[2:]
                queue_dict = {}
                result_list = []
                for queue in queue_temp_list:
                    temp_queue_dict = {}
                    queue_name = str(queue.split()[0])
                    db_queue_name = Queue_list.objects.filter(queue_name=queue_name).values('queue_name')
                    #判断数据库中是否存在，不存在插入
                    if not db_queue_name:
                        data_insert = Queue_list(queue_name=queue_name)
                        data_insert.save()
                    queue_max_run = int(queue.split()[1])
                    queue_run_job = int(queue.split()[6])
                    if queue_name == default_queue_name:
                        temp_queue_dict['is_default'] = True
                    else:
                        temp_queue_dict['is_default'] = False
                    #获取每个用户最大运行任务数
                    max_user_run_result = commands.getstatusoutput(QMGR + ' -c "list queue %s max_user_run"'%queue_name + '|grep -v "Queue %s"'%queue_name)
                    if not max_user_run_result[0] and max_user_run_result[1]:
                        max_user_run = max_user_run_result[1].split()[-1].strip()
                    else:
                        max_user_run = ''
                    #获取队列最大运行时间
                    walltime_result = commands.getstatusoutput(QMGR + ' -c "list queue %s resources_default.walltime"'%queue_name + '|grep -v "Queue %s"'%queue_name)
                    if not walltime_result[0] and walltime_result[1]:
                        walltime = walltime_result[1].split()[-1].strip()
                    else:
                        walltime = '1:00:00'
                    #获取队列优先级
                    priority_result = commands.getstatusoutput(QMGR + ' -c "list queue %s Priority"'%queue_name + '|grep -v "Queue %s"'%queue_name)
                    if not priority_result[0] and priority_result[1]:
                        Priority = priority_result[1].split()[-1].strip()
                    else:
                        Priority = 0
                    #获取节点访问控制是否启用
                    acl_host_enable_result = commands.getstatusoutput(QMGR + ' -c "list queue %s acl_host_enable"'%queue_name + '|grep -v "Queue %s"'%queue_name)
                    if not acl_host_enable_result[0] and acl_host_enable_result[1]:
                        acl_host_enable_status = acl_host_enable_result[1].split()[-1].strip()
                        if lower(acl_host_enable_status) == 'true':
                            acl_host_enable = True
                        else:
                            acl_host_enable = False
                    else:
                        acl_host_enable = False
                    #获取队列可访问节点,结果逗号分隔
                    acl_hosts_result = commands.getstatusoutput(QMGR + ' -c "list queue %s acl_hosts"'%queue_name + '|grep -v "Queue %s"'%queue_name)
                    if not acl_hosts_result[0] and acl_hosts_result[1]:
                        acl_hosts = acl_hosts_result[1].split()[-1].strip()
                    else:
                        acl_hosts = ''

                    #获取队列是否启用并且可以被调度
                    enabled_result = commands.getstatusoutput(QMGR + ' -c "list queue %s enabled"'%queue_name + '|grep -v "Queue %s"'%queue_name)
                    started_result = commands.getstatusoutput(QMGR + ' -c "list queue %s started"'%queue_name + '|grep -v "Queue %s"'%queue_name)
                    if not enabled_result[0] and not enabled_result[0] and enabled_result[1] and started_result[1]:
                        queue_enabled = enabled_result[1].split()[-1].strip()
                        started_result = enabled_result[1].split()[-1].strip()
                        if lower(queue_enabled) == "true" and lower(started_result) == 'true':
                            queue_is_enable = True
                        else:
                            queue_is_enable = False
                    else:
                        queue_is_enable = False
                    #获取用户访问控制是否启用
                    acl_user_enable_result = commands.getstatusoutput(QMGR + ' -c "list queue %s acl_user_enable"'%queue_name + '|grep -v "Queue %s"'%queue_name)
                    if not acl_user_enable_result[0] and acl_user_enable_result[1]:
                        acl_user_enable_status = acl_user_enable_result[1].split()[-1].strip()
                        if lower(acl_user_enable_status) == 'true':
                            acl_user_enable = True
                        else:
                            acl_user_enable = False
                    else:
                        acl_user_enable = False
                    #获取队列可访问用户,结果逗号分隔
                    acl_users_result = commands.getstatusoutput(QMGR + ' -c "list queue %s acl_users"'%queue_name + '|grep -v "Queue %s"'%queue_name)
                    if not acl_users_result[0] and acl_users_result[1]:
                        acl_users = acl_users_result[1].split()[-1].strip()
                    else:
                        acl_users = ''
                    temp_queue_dict['queue_name'] = queue_name
                    temp_queue_dict['max_user_run'] = max_user_run
                    temp_queue_dict['walltime'] = walltime
                    temp_queue_dict['Priority'] = Priority
                    temp_queue_dict['acl_host_enable'] = acl_host_enable
                    temp_queue_dict['acl_hosts'] = acl_hosts
                    temp_queue_dict['queue_is_enable'] = queue_is_enable
                    temp_queue_dict['acl_user_enable'] = acl_user_enable
                    temp_queue_dict['acl_users'] = acl_users
                    temp_queue_dict['queue_max_run'] = queue_max_run
                    temp_queue_dict['queue_run_job'] = queue_run_job
                    result_list.append(temp_queue_dict)
                total = Queue_list.objects.all().count()
                queue_dict['rows'] = result_list
                queue_dict['total'] = total
                queue_dict = json.dumps(queue_dict)
                return HttpResponse(queue_dict)
            except Exception:
                return HttpResponse('failed')
        else:
            return HttpResponse('failed')
    else:
        return HttpResponse(u'非法操作')

def create_queue(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse(u'非法操作')
    if req.method == 'POST':
        try:
            #判断pbs server是否启动，为0代表启动
            pbs_server_status = commands.getstatusoutput(QMGR + ' -c "list server"')
            if pbs_server_status[0]:
                return HttpResponse('failed')
            #判断队列名不能为空
            queue_name = req.POST.get('create_queue_name',None)
            if not queue_name:
                return HttpResponse('failed')
            #如果队列不存在，创建队列
            commands.getoutput(QMGR + ' -c "create queue %s"'%queue_name)
            commands.getoutput(QMGR + ' -c "set queue %s queue_type = Execution"'%queue_name)
            queue_max_run = req.POST.get('create_queue_max_run',None)
            max_user_run = req.POST.get('create_max_user_run',None)
            walltime = req.POST.get('create_max_run_time',None)
            Priority = req.POST.get('create_queue_nice',None)
            acl_host_enable = req.POST.get('create_acl_host_enable',None)
            acl_hosts = req.POST.get('create_acl_hosts',None)
            is_default = req.POST.get('create_is_default',None)
            queue_is_enable = req.POST.get('create_queue_is_enable',None)
            acl_user_enable = req.POST.get('create_acl_user_enable',None)
            acl_users = req.POST.get('create_acl_users',None)
            #如果max_running不为空
            if queue_max_run:
                commands.getoutput(QMGR + ' -c "set queue %s max_running = %s"'%(queue_name,queue_max_run))
            else:
                commands.getoutput(QMGR + ' -c "unset queue %s max_running"'%(queue_name))
            #判断用户最大运行数
            if max_user_run:
                commands.getoutput(QMGR + ' -c "set queue %s max_user_run = %s"'%(queue_name,max_user_run))
            else:
                commands.getoutput(QMGR + ' -c "unset queue %s max_user_run"'%(queue_name))
            #队列最大运行时间
            if walltime:
                commands.getoutput(QMGR + ' -c "set queue %s resources_default.walltime = %s"'%(queue_name,walltime))
            else:
                commands.getoutput(QMGR + ' -c "unset queue %s resources_default.walltime"'%(queue_name))
            #队列优先级
            if Priority == '0':
                commands.getoutput(QMGR + ' -c "set queue %s Priority = -20"'%(queue_name))
            elif Priority == '1':
                commands.getoutput(QMGR + ' -c "set queue %s Priority = 0"'%(queue_name))
            elif Priority == '2':
                commands.getoutput(QMGR + ' -c "set queue %s Priority = 19"'%(queue_name))
            #判断主机访问控制列表是否启用
            if acl_host_enable == '0':
                commands.getoutput(QMGR + ' -c "set queue %s acl_host_enable = True"'%(queue_name))
                #如果主机列表不为空，循环列表，如果为空，取消设置
                if acl_hosts:
                    for host in acl_hosts.split(','):
                        commands.getoutput(QMGR + ' -c "set queue %s acl_hosts += %s"'%(queue_name,host))   
                else:
                    commands.getoutput(QMGR + ' -c "unset queue %s acl_hosts "'%(queue_name))
            else:
                #如果acl_host_enable为1，取消设置
                commands.getoutput(QMGR + ' -c "unset queue %s acl_host_enable"'%(queue_name))
                commands.getoutput(QMGR + ' -c "unset queue %s acl_hosts "'%(queue_name))
            #判断是否默认队列
            if is_default == '0':
                commands.getoutput(QMGR + ' -c "set server default_queue = %s"'%(queue_name))
            #判断队列是否启用
            if queue_is_enable == '0':
                commands.getoutput(QMGR + ' -c "set queue %s enabled = True"'%(queue_name))
                commands.getoutput(QMGR + ' -c "set queue %s started = True"'%(queue_name))
            elif queue_is_enable == '1':
                commands.getoutput(QMGR + ' -c "set queue %s enabled = False"'%(queue_name))
                commands.getoutput(QMGR + ' -c "set queue %s started = False"'%(queue_name))
            #判断用户访问控制列表是否启用
            if acl_user_enable == '0':
                commands.getoutput(QMGR + ' -c "set queue %s acl_user_enable = True"'%(queue_name))
                #如果用户列表不为空，循环列表，如果为空，取消设置
                if acl_users:
                    commands.getoutput(QMGR + ' -c "unset queue %s acl_users "'%(queue_name))
                    for user in acl_users.split(','):
                        #commands.getoutput(QMGR + ' -c "unset queue %s acl_users "'%(queue_name))
                        commands.getoutput(QMGR + ' -c "set queue %s acl_users += %s"'%(queue_name,user))
                else:
                    commands.getoutput(QMGR + ' -c "unset queue %s acl_users "'%(queue_name))
            else:
                #如果acl_user_enable为1，取消设置
                commands.getoutput(QMGR + ' -c "unset queue %s acl_user_enable"'%(queue_name))
                commands.getoutput(QMGR + ' -c "unset queue %s acl_users "'%(queue_name))
            return HttpResponse('ok')
        except Exception,e:
            return HttpResponse('failed')
    else:
        return HttpResponse(u'非法操作')
    
def del_queue(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse(u'非法操作')
    if req.method == 'POST':
        try:
            queue_name = req.POST.get('queue_name',None)
            commands.getoutput(QMGR + ' -c "delete queue %s"'%queue_name)
            row_data = Queue_list.objects.get(queue_name=queue_name)
            row_data.delete()
            return HttpResponse('ok')
        except Exception:
            return HttpResponse('failed')
    else:
        return HttpResponse(u'非法操作')
    
def mgr_node_sched_index(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse(u'非法操作')
    return render(req,'schedmgr/mgr_node_sched.html')

def get_node_sched(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse(u'非法操作')
    if req.method == 'POST':
        try:
            node_data = Host.objects.only('host_name').order_by('id')
            total = Host.objects.all().count()
            node_sched_dict = {}
            node_sched_list = []
            for i in node_data:
                temp_node_sched_dict = {}
                host_name = i.host_name
                #pbsnodes获取节点信息
                node_sched_cmd = PBSNODES + ' -q ' + host_name
                node_sched_result = commands.getoutput(node_sched_cmd)
                #通过pestat获取节点负载
                node_pestat_cmd = PESTAT + '|grep %s' %host_name
                node_pestat_result = commands.getoutput(node_pestat_cmd)
                host_id = Host.objects.filter(host_name=host_name).values('id')[0].values()[0]
                host_mem = Mem.objects.filter(host_name_id=host_id).values()
                #判断pbsnode是否能够获取节点信息
                if node_sched_result:
                    try:
                        node_stats = node_sched_result.split('\n')[1].split('=')[-1].strip()
                        config_ncpus = commands.getoutput(PBSNODES +' -q %s'%host_name +'|grep "np ="')
                        config_ncpus = config_ncpus.split('=')[-1].strip()
                        #判断pbsnodes是否有job运行
                        node_jobs = commands.getoutput(PBSNODES +' -q %s'%host_name +'|grep "jobs ="')
                        if node_jobs.split('=')[0].strip() == 'jobs':
                            node_jobs = node_jobs.split('=')[1].strip()
                        else:
                            node_jobs = ''
                    except Exception:
                        node_stats = u'无法获取数据'
                        config_ncpus = u'无法获取数据'
                        node_jobs = u'无法获取数据'
                        
                else:
                    node_stats = u'调度未配置'
                    config_ncpus = u'调度未配置'
                    node_jobs = u'调度未配置'
                #判断pestat能否获取主机数据
                if node_pestat_result:
                    try:
                        node_load = node_pestat_result.split()[2]
                    except Exception:
                        node_load = u'无法获取数据'
                else:
                    node_load = u'未知'
                #是否正确获取主机内存
                if host_mem:
                    mem_percent = u'已使用' + host_mem[0]['mem_percent'] + '%'
                    mem_total = host_mem[0]['mem_total'] + 'MB'
                else:
                    mem_percent = ''
                    mem_total = ''
                temp_node_sched_dict['node_stats'] = node_stats
                temp_node_sched_dict['config_ncpus'] = config_ncpus
                temp_node_sched_dict['node_load'] = node_load
                temp_node_sched_dict['mem_total'] = mem_total
                temp_node_sched_dict['node_jobs'] = node_jobs
                temp_node_sched_dict['mem_percent'] = mem_percent
                temp_node_sched_dict['host_name']= host_name
                node_sched_list.append(temp_node_sched_dict)
            node_sched_dict['rows'] = node_sched_list
            node_sched_dict['total'] = total
            node_sched_dict = json.dumps(node_sched_dict)
            return HttpResponse(node_sched_dict)
        except Exception:
            return HttpResponse('failed')
    else:
        return HttpResponse(u'非法操作')

def mgr_node_sched(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse(u'非法操作')
    if req.method == 'POST':
        service_oper = req.POST.get('oper_type',None)
        host_name_list = req.POST.get('host_name',None)
        failed_host = ''
        succ_host = ''
        try:
            for host_name in host_name_list.split(','):
                host_name = str(host_name)
                cmd = exec_commands(connect(host_name,'root'),'/etc/init.d/pbs_mom  %s'%service_oper)
                print cmd
                if cmd == 'failed':
                    failed_host = failed_host + host_name + ','
                else:
                    succ_host = succ_host + host_name + ','
            if failed_host:
                tip_msg = u'主机:'+ failed_host + u'操作失败' 
            else:
                tip_msg = u'主机:' + succ_host +  u'操作成功'
            return HttpResponse(tip_msg)
        except Exception,e:
            return HttpResponse(e)
    else:
        return HttpResponse(u'非法操作')
    
def mgr_sched_index(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse(u'非法操作')
    pbs_service_dict = {PBS_SERVER:['pbs_server',PBS_HOME,'pbs'],PBS_MOM:['pbs_mom',PBS_HOME,'pbs'],MAUI_HOME:['maui',PBS_SCHED,'maui']}
    for service_data in pbs_service_dict.keys():
        sched_service_data = Sched_service_list.objects.all().filter(service_process=service_data)
        if not sched_service_data:
            service_name = pbs_service_dict[service_data][0]
            service_home = pbs_service_dict[service_data][1]
            service_type = pbs_service_dict[service_data][2]
            data_insert = Sched_service_list(service_name=service_name,service_home=service_home,service_type=service_type,service_process=service_data)
            data_insert.save()
    return render(req,'schedmgr/mgr_sched_service.html')

def get_sched_service(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse(u'非法操作')
    if req.method == 'POST':
        sched_service_list = []
        sched_service_dict = {}
        try:
            sched_service_data = Sched_service_list.objects.all()
            for sched_service in sched_service_data:
                temp_sched_dict = {}
                cmd = 'ps aux|grep %s|grep -v grep' %sched_service.service_name
                cmd_result = commands.getoutput(cmd)
                if cmd_result:
                    temp_sched_dict['service_process_num'] = cmd_result.split()[1]
                    temp_sched_dict['servcie_status'] = u'运行'
                    temp_sched_dict['service_info'] = u'可用'
                else:
                    temp_sched_dict['servcie_status'] = u'未运行'
                    temp_sched_dict['service_info'] = u'不可用'
                    temp_sched_dict['service_process_num'] = ''
                temp_sched_dict['service_name'] = sched_service.service_name
                temp_sched_dict['service_home'] = sched_service.service_home
                temp_sched_dict['service_type'] = sched_service.service_type
                temp_sched_dict['service_process'] = sched_service.service_process
                sched_service_list.append(temp_sched_dict)
            sched_service_dict['rows'] = sched_service_list
            sched_service_dict = json.dumps(sched_service_dict)
            return HttpResponse(sched_service_dict)
        except Exception:
            return HttpResponse('failed')
    else:
        return HttpResponse(u'非法操作')

def mgr_sched_service(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse(u'非法操作')
    if req.method == 'POST':
        service_oper = req.POST.get('oper_type',None)
        service_process = req.POST.get('service_process',None)  
        #service_process :  '/opt/xxx/yy/pbs_server' 
        service_name = os.path.basename(service_process)       
        try:
            cmd = commands.getstatusoutput('/etc/init.d/' + service_name + '  ' +service_oper)
            if not cmd[0]:
                return HttpResponse('ok')
            else:
                return HttpResponse('failed')
        except Exception:
            return HttpResponse('failed')
    else:
        return HttpResponse(u'非法操作')


def mgr_user_sched_index(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse(u'非法操作')
    return render(req,'schedmgr/mgr_user_sched.html')
        
def get_user_sched(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
            return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse(u'非法操作')
    if req.method == 'POST':
        try:
            user_sched_dict = {}
            user_sched_list = []
            user_max_node = ''
            user_max_core = ''
            user_max_job = ''
            user_data = User.objects.only('user_name').order_by('id')
            total = User.objects.all().count() - 1
            for i in user_data:
                if i.user_name != 'superuser':
                    temp_user_sched_dict = {}
                    user_name = i.user_name
                    #获取用户信息
                    with open(MAUI_CFG,'r') as r:
                        lines=r.readlines()
                        for l in lines:
                            if l.strip() and l.strip().startswith('USERCFG[%s]'%user_name):
                                for i in l.strip().split():
                                    if i.strip().startswith('MAXNODE'):
                                        user_max_node = i.strip().split('=')[-1]
                                    if i.strip().startswith('MAXPROC'):
                                        user_max_core = i.strip().split('=')[-1]
                                    if i.strip().startswith('MAXJOB'):
                                        user_max_job = i.strip().split('=')[-1]
                    acl_queue_list = []
                    #获取队列名
                    cmd = commands.getoutput(QSTAT +' -Q')
                    queue_temp_list = cmd.split('\n')[2:]
                    for queue in queue_temp_list:
                        queue_name = str(queue.split()[0])
                        user_acl_result = commands.getoutput(QMGR + ' -c "list queue %s acl_users"'%queue_name).split()
                        user_acl_enable_result = commands.getoutput(QMGR + ' -c "list queue %s acl_user_enable"'%queue_name).split()
                        if user_acl_enable_result[-1] == 'False' or len(user_acl_enable_result) == 2:    #如果acl_user_eanble禁用，不管acl_users是否有值，用户可以访问队列
                            acl_queue_list.append(queue_name)
                        elif len(user_acl_result) > 2:               #如果acl_users有值，并且用户在acl_users中，无论acl_user_enable是否启用，用户都可以访问队列
                            acl_users = user_acl_result[-1]
                            if  user_name in acl_users:
                                acl_queue_list.append(queue_name)
                        elif len(user_acl_result) <= 2 and user_acl_enable_result[-1] != 'True':   #如果acl_users没有值，并且acl_user_enable不为True
                            acl_queue_list.append(queue_name)
                    temp_user_sched_dict['user_name'] = user_name
                    temp_user_sched_dict['user_max_node'] = user_max_node
                    temp_user_sched_dict['user_max_core'] = user_max_core
                    temp_user_sched_dict['user_max_job'] = user_max_job
                    temp_user_sched_dict['acl_queue'] = acl_queue_list
                    user_sched_list.append(temp_user_sched_dict)
            user_sched_dict['rows'] = user_sched_list
            user_sched_dict['total'] = total
            user_sched_dict = json.dumps(user_sched_dict)
            return HttpResponse(user_sched_dict)
        except Exception:
            return HttpResponse('failed')
    else:
        return HttpResponse(u'非法操作')

def modify_user_sched(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    if req.method == 'POST':
        try:
            user_name = req.POST.get('user_name', None)
            user_max_node = req.POST.get('user_max_node', None)
            user_max_core = req.POST.get('user_max_core', None)
            user_max_job = req.POST.get('user_max_job', None)
            acl_queue = req.POST.get('acl_queue', None)
            #防止更改用户名提交
            if not user_name:
                return HttpResponse('failed')
            #修改maui中的行,如果maxnode，maxproc，maxjob都为空，不进行如何更改
            if user_max_node or user_max_core or user_max_job:
                #中间有任意一值不为空，做字符串拼接
                if user_max_node:
                    MAXNODE_RESULT  = 'MAXNODE=%s'%user_max_node
                else:
                    MAXNODE_RESULT = ''
                if user_max_core:
                    MAXPROC_RESULT  = 'MAXPROC=%s'%user_max_core
                else:
                    MAXPROC_RESULT  = ''
                if user_max_job:
                    MAXJOB_RESULT = 'MAXJOB=%s'%user_max_job
                else:
                    MAXJOB_RESULT = ''
                #修改配置文件
                usercfg_is_exsits = False
                with open(MAUI_CFG,'r') as r:
                    file_lines=r.readlines()
                with open(MAUI_CFG,'w') as w:
                    for l in file_lines:
                        if l.strip().startswith('USERCFG[%s]'%user_name):
                            usercfg_is_exsits = True
                            index_num = file_lines.index(l)
                            file_lines[index_num] = 'USERCFG[%s]'%user_name + ' ' +  MAXNODE_RESULT + ' ' +  MAXPROC_RESULT + ' ' +  MAXJOB_RESULT + '\n'
                            w.write(file_lines[index_num])
                        else:
                            w.write(l)  
                    if not usercfg_is_exsits:
                        add_lines = 'USERCFG[%s]'%user_name + ' ' +  MAXNODE_RESULT + ' ' +  MAXPROC_RESULT + ' ' +  MAXJOB_RESULT + '\n'
                        w.write(add_lines)   
            #如果每项都为空，判断是否文件有这一行，如果有，删除    
            else:
                with open(MAUI_CFG,'r') as r:
                    file_lines=r.readlines()
                with open(MAUI_CFG,'w') as w:
                    for l in file_lines:
                        if l.strip().startswith('USERCFG[%s]'%user_name):
                            index_num = file_lines.index(l)
                            del file_lines[index_num:index_num]
                        else:
                            w.write(l)
            #获取队列名，删除用户可以访问的队列
            cmd = commands.getoutput(QSTAT +' -Q')
            queue_temp_list = cmd.split('\n')[2:]
            for queue in queue_temp_list:
                queue_name = str(queue.split()[0])
                commands.getoutput(QMGR + ' -c "set queue %s acl_users -= %s"'%(queue_name, user_name))
            #添加用户可访问队列
            if acl_queue:
                for queue_name in acl_queue.split(','):
                    commands.getoutput(QMGR + ' -c "set queue %s acl_users += %s"'%(queue_name, user_name))
            cmd = commands.getstatusoutput('/etc/init.d/maui restart')
            if not cmd[0]:
                return HttpResponse('ok')
            else:
                return HttpResponse('failed')
        except Exception:
            return HttpResponse('failed')
    else:
        return HttpResponse(u'非法操作')
