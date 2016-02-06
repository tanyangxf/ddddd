#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
import json
import commands
import os
import subprocess
from models import Job_list
# Create your views here.
def index(req):
    return render_to_response('index.html')

def new_job(req):
    if req.method == 'POST':
        try:
            data = req.POST
            qsub_command = "echo '%s'|qsub" %(data['job_name'])
            qsub_submit = commands.getoutput(qsub_command)
            qstat_command = "qstat -a"
            result = commands.getoutput(qstat_command)
            return HttpResponse(json.dumps(result))
        except Exception,e:
            print e
            return HttpResponse(e)
    else:
        result = Job_list.objects.all()
        result_list = []
        for i in result:
            temp_dict={}
            temp_dict['job_id'] = i.job_id
            temp_dict['job_name'] = i.job_name
            temp_dict['job_user_name'] = i.job_user_name
            temp_dict['job_queue'] = i.job_queue
            temp_dict['job_start_time'] = i.job_start_time
            temp_dict['job_run_time'] = i.job_run_time
            temp_dict['job_status'] = i.job_status
            result_list.append(temp_dict)
        return render_to_response('job/new_job.html',{'job_data':result_list})

def job_mgr(req):
    if req.method == 'POST':
        data = req.POST
        result = subprocess.check_output(data['dat'],shell=True)
        #返回给ajax的arg参数
        #result = result.decode('gbk','replace')
        #return HttpResponse(json.dumps(data))
        return HttpResponse(json.dumps(result))
    else:
        return render_to_response('job/job_mgr.html')
