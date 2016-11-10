#coding:utf-8
import json
from django.shortcuts import HttpResponse,redirect
import commands

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

def get_queue_tree(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('login')
    queue = u"队列列表"
    queuetree = {'id':'all_queue'}
    queuetree['children'] = []
    queuetree['text'] = queue
    queuetree['icon'] = "glyphicon glyphicon-folder-close"
    #提前定义数据格式
    data = {}
    cmd = commands.getoutput(QSTAT +' -Q')
    try:
        queue_temp_list = cmd.split('\n')[2:]
    except Exception:
        return HttpResponse('failed')
    for queue in queue_temp_list:
        queue_name = str(queue.split()[0])
        data = {"id":queue_name,"text":queue_name,"children":False,"icon":"glyphicon glyphicon-file"}
        queuetree['children'].append(data)
    queuetree = json.dumps(queuetree)
    return HttpResponse(queuetree)
