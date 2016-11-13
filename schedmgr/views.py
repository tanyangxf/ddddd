#coding:utf-8
from django.shortcuts import render,HttpResponse, redirect
import commands
from monitor.models import Host,Mem
from string import lower
import json
from sysmgr.models import User
# Create your views here.
PESTAT = '/usr/bin/pestat'
PBSNODES = '/torque2.4/bin/pbsnodes'
QSUB = '/torque2.4/bin/qsub'
QDEL= '/torque2.4/bin/qdel'
QSTAT = '/torque2.4/bin/qstat'
QHOLD = '/torque2.4/bin/qhold'
QMGR = '/torque2.4/bin/qmgr'
PBS_HOME = '/torque2.4'
PBS_SERVER = '/torque2.4/bin/pbs_server'
PBS_MOM = '/torque2.4/bin/pbs_mom'
PBS_SCHED = '/usr/local/maui-3.3.1/sbin/maui'
MAUI_CFG = '/usr/local/maui/maui.cfg'

def queue_tree(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    return render(req,'schedmgr/queue_tree.html')

#{'high':{"max_job":0,"run_job":0,default_queue:'true'},'low':}
def mgr_queue(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse('failed')
    cmd = commands.getoutput(QSTAT +' -Q')
    try:
        default_queue = commands.getoutput(QMGR + ' -c "list server default"|grep default_queue')
        default_queue_name = default_queue.split('=')[1].strip()
        queue_temp_list = cmd.split('\n')[2:]
    except Exception:
        return HttpResponse('failed')
    queue_dict = {}
    for queue in queue_temp_list:
        temp_queue_dict = {}
        queue_name = str(queue.split()[0])
        #queue_max_run = int(queue.split()[1])
        queue_run_job = int(queue.split()[6])
        if queue_name == default_queue_name:
            temp_queue_dict['is_default'] = u'是'
        else:
            temp_queue_dict['is_default'] = u'否'
        #temp_queue_dict['queue_max_run'] = queue_max_run
        temp_queue_dict['queue_run_job'] = queue_run_job
        queue_dict[queue_name] = temp_queue_dict
    return render(req,'schedmgr/mgr_queue.html',{'queue_dict':queue_dict})

def get_queue(req):
    req.session.set_expiry(1800)
    if req.method == 'POST':
        queue_data = {}
        queue_name = req.POST.get('queue_name', None)
        #获取最大运行任务数
        max_running_result = commands.getstatusoutput(QMGR + ' -c "list queue %s max_running"'%queue_name + '|grep -v "Queue %s"'%queue_name)
        if not max_running_result[0] and max_running_result[1]:
            max_running = max_running_result[1].split()[-1].strip()
        else:
            max_running = ''
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
        #获取默认队列
        default_queue_result = commands.getstatusoutput(QMGR + ' -c "list server default_queue"')
        if not default_queue_result[0] and default_queue_result[1]:
            default_queue_name = default_queue_result[1].split()[-1].strip()
            if queue_name == default_queue_name:
                default_queue = True
            else:
                default_queue = False
                
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
        queue_data['queue_name'] = queue_name
        queue_data['max_running'] = max_running
        queue_data['max_user_run'] = max_user_run
        queue_data['walltime'] = walltime
        queue_data['Priority'] = Priority
        queue_data['acl_host_enable'] = acl_host_enable
        queue_data['acl_hosts'] = acl_hosts
        queue_data['default_queue'] = default_queue
        queue_data['queue_is_enable'] = queue_is_enable
        queue_data['acl_user_enable'] = acl_user_enable
        queue_data['acl_users'] = acl_users
        queue_data = json.dumps(queue_data)
        return HttpResponse(queue_data)
    else:
        user_dict = req.session.get('is_login', None)
        if not user_dict:
            return redirect('/login')
        return HttpResponse('not data')    

def create_queue(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    if req.method == 'POST':
        #判断pbs server是否启动，为0代表启动
        pbs_server_status = commands.getstatusoutput(QMGR + ' -c "list server"')
        if pbs_server_status[0]:
            return HttpResponse('failed')
        #判断队列名不能为空
        queue_name = req.POST.get('queue_name',None)
        if not queue_name:
            return HttpResponse('queue_failed')
        #如果队列不存在，创建队列
        commands.getoutput(QMGR + ' -c "create queue %s"'%queue_name)
        commands.getoutput(QMGR + ' -c "set queue %s queue_type = Execution"'%queue_name)
        max_running = req.POST.get('max_running',None)
        max_user_run = req.POST.get('max_user_run',None)
        walltime = req.POST.get('walltime',None)
        Priority = req.POST.get('Priority',None)
        acl_host_enable = req.POST.get('acl_host_enable',None)
        acl_hosts = req.POST.get('acl_hosts',None)
        default_queue = req.POST.get('default_queue',None)
        queue_is_enable = req.POST.get('queue_is_enable',None)
        acl_user_enable = req.POST.get('acl_user_enable',None)
        acl_users = req.POST.get('acl_users',None)
        #如果max_running不为空
        if max_running:
            commands.getoutput(QMGR + ' -c "set queue %s max_running = %s"'%(queue_name,max_running))
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
                try:
                    for host in acl_hosts.split(','):
                        commands.getoutput(QMGR + ' -c "set queue %s acl_hosts += %s"'%(queue_name,host))
                except:
                    return HttpResponse('host_failed')    
            else:
                commands.getoutput(QMGR + ' -c "unset queue %s acl_hosts "'%(queue_name))
        else:
            #如果acl_host_enable为1，取消设置
            commands.getoutput(QMGR + ' -c "unset queue %s acl_host_enable"'%(queue_name))
            commands.getoutput(QMGR + ' -c "unset queue %s acl_hosts "'%(queue_name))
        #判断是否默认队列
        if default_queue == '0':
            commands.getoutput(QMGR + ' -c "set server default_queue = %s"'%(queue_name))
        #判断队列是否启用
        print queue_is_enable
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
                try:
                    for user in acl_users.split(','):
                        commands.getoutput(QMGR + ' -c "unset queue %s acl_users "'%(queue_name))
                        commands.getoutput(QMGR + ' -c "set queue %s acl_users += %s"'%(queue_name,user))
                except:
                    return HttpResponse('user_failed')    
            else:
                commands.getoutput(QMGR + ' -c "unset queue %s acl_users "'%(queue_name))
        else:
            #如果acl_user_enable为1，取消设置
            commands.getoutput(QMGR + ' -c "unset queue %s acl_user_enable"'%(queue_name))
            commands.getoutput(QMGR + ' -c "unset queue %s acl_users "'%(queue_name))
        return HttpResponse('ok')
    return HttpResponse('no data')
    
def del_queue(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    if req.method == 'POST':
        queue_name = req.POST.get('queue_name',None)
        commands.getoutput(QMGR + ' -c "delete queue %s"'%queue_name)
        return HttpResponse('ok')
    return HttpResponse('not change')
def mgr_node_sched(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse('failed')
    node_data = Host.objects.only('host_name').order_by('id')
    all_sched_dict = {}
    for i in node_data:
        node_sched_dict = {}
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
            node_stats = node_sched_result.split('\n')[1].split('=')[-1].strip()
            config_ncpus = commands.getoutput('pbsnodes -q %s'%host_name +'|grep "np ="')
            config_ncpus = config_ncpus.split('=')[-1].strip()
            #判断pbsnodes是否有job运行
            node_jobs = commands.getoutput('pbsnodes -q %s'%host_name +'|grep "jobs ="')
            if node_jobs.split('=')[0].strip() == 'jobs':
                node_jobs = node_jobs.split('=')[1].strip()
            else:
                node_jobs = ''
        else:
            node_stats = u'调度未配置'
            config_ncpus = u'调度未配置'
            node_jobs = u'调度未配置'
        #判断pestat能否获取主机数据
        if node_pestat_result:
            node_load = node_pestat_result.split()[2]
        else:
            node_load = u'未知'
        #是否正确获取主机内存
        if host_mem:
            mem_use_percent = u'已使用' + host_mem[0]['mem_percent'] + '%'
            mem_total = host_mem[0]['mem_total'] + 'MB'
        else:
            mem_use_percent = ''
            mem_total = ''
        node_sched_dict['node_stats'] = node_stats
        node_sched_dict['config_ncpus'] = config_ncpus
        node_sched_dict['node_load'] = node_load
        node_sched_dict['mem_total'] = mem_total
        node_sched_dict['node_jobs'] = node_jobs
        node_sched_dict['mem_use_percent'] = mem_use_percent
        all_sched_dict[host_name]= node_sched_dict
    return render(req,'schedmgr/mgr_node_sched.html',{'all_sched_dict':all_sched_dict})

def mgr_sched_service(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse('failed')
    pbs_service_list = [PBS_SERVER,PBS_MOM,PBS_SCHED]
    pbs_service_dict = {}
    for pbs_service in pbs_service_list:
        pbs_temp_dict = {}
        pbs_temp_dict['pbs_type'] = 'pbs'
        pbs_temp_dict['pbs_home'] = PBS_HOME
        pbs_temp_dict['pbs_process'] = pbs_service
        if pbs_service == PBS_SERVER:
            pbs_service_name= u'pbs主服务'
            service_name = 'pbs_server'
            pbs_service_name
        elif pbs_service == PBS_MOM:
            pbs_service_name = u'pbs计算服务'
            service_name = 'pbs_mom'
        elif pbs_service == PBS_SCHED:
            pbs_service_name = u'pbs调度服务'
            pbs_temp_dict['pbs_home'] = '/usr/local/maui-3.3.1/'
            service_name = 'maui'
        cmd = 'ps aux|grep %s|grep -v grep' %service_name
        cmd_result = commands.getoutput(cmd)
        if cmd_result:
            pbs_temp_dict['service_process_num'] = cmd_result.split()[1]
            pbs_temp_dict['pbs_servcie_status'] = u'运行'
            pbs_temp_dict['pbs_service_info'] = u'可用'
        else:
            pbs_temp_dict['pbs_servcie_status'] = u'未运行'
            pbs_temp_dict['pbs_service_info'] = u'不可用'
            pbs_temp_dict['service_process_num'] = ''
        pbs_service_dict[pbs_service_name] = pbs_temp_dict
    return render(req,'schedmgr/mgr_sched_service.html',{'pbs_service_dict':pbs_service_dict})
            
def mgr_user_sched(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    if req.method == 'POST':
        user_name = req.POST.get('user_name', None)
        user_sched_dict = {}
        user_max_node = ''
        user_max_core = ''
        user_max_job = ''
        #获取就节点状态
        with open(MAUI_CFG,'r') as r:
            lines=r.readlines()
            for l in lines:
                if l.strip().startswith('USERCFG[%s]'%user_name):
                    for i in l.strip().split():
                        if i.strip().startswith('MAXNODE'):
                            user_max_node = i.strip().split('=')[-1]
                        if i.strip().startswith('MAXPROC'):
                            user_max_core = i.strip().split('=')[-1]
                        if i.strip().startswith('MAXJOB'):
                            user_max_job = i.strip().split('=')[-1]
        queue_acl_list = []
        #获取队列名
        cmd = commands.getoutput(QSTAT +' -Q')
        try:
            queue_temp_list = cmd.split('\n')[2:]
        except Exception:
            return HttpResponse('failed')
        for queue in queue_temp_list:
            queue_name = str(queue.split()[0])
            user_acl_result = commands.getoutput(QMGR + ' -c "list queue %s acl_users"'%queue_name).split()
            user_acl_enable_result = commands.getoutput(QMGR + ' -c "list queue %s acl_user_enable"'%queue_name).split()
            if user_acl_enable_result[-1] == 'False':    #如果acl_user_eanble禁用，不管acl_users是否有值，用户可以访问队列
                queue_acl_list.append(queue_name)
            elif len(user_acl_result) > 2:               #如果acl_users有值，并且用户在acl_users中，无论acl_user_enable是否启用，用户都可以访问队列
                acl_users = user_acl_result[-1]
                if  user_name in acl_users:
                    queue_acl_list.append(queue_name)
            elif len(user_acl_result) <= 2 and user_acl_enable_result[-1] != 'True':   #如果acl_users没有值，并且acl_user_enable不为True
                queue_acl_list.append(queue_name)
        user_sched_dict['user_name'] = user_name
        user_sched_dict['user_max_node'] = user_max_node
        user_sched_dict['user_max_core'] = user_max_core
        user_sched_dict['user_max_job'] = user_max_job
        user_sched_dict['queue_acl'] = queue_acl_list
        data = json.dumps(user_sched_dict)
        return HttpResponse(data)
    else:
        user_data = User.objects.only('user_name').order_by('id')
        user_dict = {}
        for i in user_data:
            if i.user_name != 'superuser':
                user_name = i.user_name
                user_dict[user_name] = ''
        return render(req,'schedmgr/mgr_user_sched.html',{'user_dict':user_dict})

def modify_user_sched(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if req.method == 'POST':
        user_name = req.POST.get('user_name', None)
        user_max_node = req.POST.get('user_max_node', None)
        user_max_core = req.POST.get('user_max_core', None)
        user_max_job = req.POST.get('user_max_job', None)
        queue_acl = req.POST.get('queue_acl', None)
        #防止更改用户名提交
        if not user_name:
            return HttpResponse('user_name is null')
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
                    file_lines = 'USERCFG[%s]'%user_name + ' ' +  MAXNODE_RESULT + ' ' +  MAXPROC_RESULT + ' ' +  MAXJOB_RESULT + '\n'
                    w.write(file_lines)   
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
        #修改用户可访问队列
        if queue_acl:
            for queue_name in queue_acl.split(','):
                commands.getoutput(QMGR + ' -c "set queue %s acl_users += %s"'%(queue_name, user_name))
        return HttpResponse('ok')
    else:
        if not user_dict:
            return redirect('/login')
        return HttpResponse('no data')
