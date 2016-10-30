#coding:utf-8
from django.shortcuts import render_to_response,HttpResponse
import commands
from monitor.models import Host,Mem
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
PBS_SCHED = '/torque2.4/bin/pbs_sched'

#{'high':{"max_job":0,"run_job":0,default_queue:'true'},'low':}
def mgr_queue(req):
    cmd = commands.getoutput(QSTAT +' -Q')
    try:
        default_queue = commands.getoutput(QMGR + ' -c "list server default"|grep default_queue')
        default_queue_name = default_queue.split('=')[1].strip()
        queue_temp_list = cmd.split('\n')[2:]
    except Exception,e:
        return HttpResponse('failed')
    queue_dict = {}
    for queue in queue_temp_list:
        temp_queue_dict = {}
        queue_name = str(queue.split()[0])
        queue_max_run = int(queue.split()[1])
        queue_run_job = int(queue.split()[6])
        if queue_name == default_queue_name:
            temp_queue_dict['is_default'] = u'是'
        else:
            temp_queue_dict['is_default'] = u'否'
        temp_queue_dict['queue_max_run'] = queue_max_run
        temp_queue_dict['queue_run_job'] = queue_run_job
        queue_dict[queue_name] = temp_queue_dict
    return render_to_response('schedmgr/mgr_queue.html',{'queue_dict':queue_dict})

def mgr_node_sched(req):
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
            config_ncpus = node_sched_result.split('\n')[2].split('=')[-1].strip()
            #判断pbsnodes是否有job运行
            if node_sched_result.split('\n')[4].split('=')[0].strip() == 'jobs':
                node_jobs = node_sched_result.split('\n')[4].split('=')[-1].strip()
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
    return render_to_response('schedmgr/mgr_node_sched.html',{'all_sched_dict':all_sched_dict})

def mgr_sched_service(req):
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
            service_name = 'pbs_sched'
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
    return render_to_response('schedmgr/mgr_sched_service.html',{'pbs_service_dict':pbs_service_dict})
            


def mgr_sched_user(req):
    pass


