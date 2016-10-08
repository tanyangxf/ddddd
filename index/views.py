#coding:utf-8
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from sysmgr.models import User
import hashlib
from django.http import HttpResponse
from django.db.models import Sum
import commands
import time
import json

from job.models import Job_list
from monitor.models import *

PESTAT = '/usr/bin/pestat'
PBSNODES = '/torque2.4/bin/pbsnodes'
QSUB = '/torque2.4/bin/qsub'
QDEL= '/torque2.4/bin/qdel'
QSTAT = '/torque2.4/bin/qstat'
QHOLD = '/torque2.4/bin/qhold'

def default(req):
    return render_to_response('default.html')

def login(req):
    if req.method == 'POST':
        user_name = req.POST.get('username', None)
        password = req.POST.get('password', None)
        password = hashlib.sha1(password+user_name).hexdigest()
        #name = User.objects.get(user_name = user_name).user_name
        user = User.objects.filter(user_name=user_name,password=password)
        if user:
            name = User.objects.get(user_name = user_name).user_name
            return redirect("/index")
        else:
            return render_to_response('login.html', {'msg':'用户名或密码错误'})
    else:
        return render_to_response('login.html')
    
def index(req):
    #get pbs nodes status
    pbs_all_nodes = int(commands.getoutput(PESTAT + '|wc -l')) - 1
    #pbs_free_nodes = commands.getoutput('pbsnodes -l free|wc -l')
    pbs_down_nodes = int(commands.getoutput(PBSNODES + ' -l down|wc -l'))
    pbs_offline_nodes = int(commands.getoutput(PBSNODES + ' -l offline|wc -l'))
    pbs_unknown_nodes = int(commands.getoutput(PBSNODES + ' -l unknown|wc -l'))
    pbs_free_nodes = pbs_all_nodes - pbs_down_nodes - pbs_offline_nodes - pbs_unknown_nodes
    cluster_status = {'pbs_all_nodes':pbs_all_nodes,'pbs_free_nodes':pbs_free_nodes,
                              'pbs_down_nodes':pbs_down_nodes,'pbs_offline_nodes':pbs_offline_nodes,
                              'pbs_unknown_nodes':pbs_unknown_nodes}
    
    #get pbs queue status
    cmd = commands.getoutput(QSTAT +' -Q')
    queue_temp_list = cmd.split('\n')[2:]
    queue_dict = {}
    for queue in queue_temp_list:
        temp_queue_list = []
        queue_name = str(queue.split()[0])
        queue_max_run = int(queue.split()[1])
        queue_run_job = int(queue.split()[6])
        temp_queue_list.append(queue_max_run)
        temp_queue_list.append(queue_run_job)
        queue_dict[queue_name] = temp_queue_list
    cluster_status['queue_status'] = json.dumps(queue_dict)
    
    #获取集群cpu状态信息
    '''
    {'l_cpu_count__sum': 6}
    {'cpu_percent__sum': 13.5}
    '''
    l_cpu_count = Cpu.objects.aggregate(Sum('l_cpu_count'))
    all_cpu_percent = Cpu.objects.aggregate(Sum('cpu_percent'))
    #转换字典，添加到cluster_status字典
    cluster_status = dict(cluster_status,**l_cpu_count)
    cluster_status = dict(cluster_status,**all_cpu_percent)
        
    #get job info 
    #select job info in mysql 
    start = 0
    end = 8
    total = Job_list.objects.all().count()
    all_result = Job_list.objects.all()[start:end]       
    result_list = []
    job_status_dict = {'C':u'完成','E':u'退出','H':u'挂起','Q':u'排队','R':'运行','T':u'移动','W':u'排队','S':u'暂停'}
    for i in all_result:
        temp_dict={}
        temp_dict['job_id'] = i.job_id
        temp_dict['job_name'] = i.job_name
        temp_dict['job_user_name'] = i.job_user_name
        temp_dict['job_queue'] = i.job_queue
        temp_dict['job_start_time'] = i.job_start_time
        temp_dict['job_run_time'] = i.job_run_time
        temp_dict['job_status'] = job_status_dict[i.job_status]
        result_list.append(temp_dict)
    cluster_status['job_data'] = result_list
    if not cluster_status['job_data']:
        cluster_status['msg'] = u'没有任何任务信息！'
    return render_to_response("index.html",cluster_status)