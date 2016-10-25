#coding:utf-8
from django.shortcuts import render_to_response,HttpResponse
import commands
# Create your views here.
PESTAT = '/usr/bin/pestat'
PBSNODES = '/torque2.4/bin/pbsnodes'
QSUB = '/torque2.4/bin/qsub'
QDEL= '/torque2.4/bin/qdel'
QSTAT = '/torque2.4/bin/qstat'
QHOLD = '/torque2.4/bin/qhold'
QMGR = '/torque2.4/bin/qmgr'
#{'high':{"max_job":0,"run_job":0,default_queue:'true'},'low':}
def mgr_queue(req):
    cmd = commands.getoutput(QSTAT +' -Q')
    default_queue = commands.getoutput(QMGR + ' -c "list server default"|grep default_queue')
    default_queue_name = default_queue.split('=')[1].strip()
    queue_temp_list = cmd.split('\n')[2:]
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
    print queue_dict
    return render_to_response('schedmgr/mgr_queue.html',{'queue_dict':queue_dict})

def mgr_sched(req):
    pass

def mgr_sched_user(req):
    pass

def mgr_sched_node(req):
    pass
