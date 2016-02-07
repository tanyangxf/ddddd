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
            userInput = req.POST
            #pbs subcommit command
            qsub_command = "echo '%s'|qsub" %(userInput['job_name'])
            #submit job
            qsub_submit = commands.getoutput(qsub_command)
            #get job_id
            job_id = qsub_submit.split('.')[0]
            #get job detal command
            qstat_command = "qstat -f %s" % job_id
            #get job detal result
            qstat_result = commands.getoutput(qstat_command)
            #回车分割变成列表
            qstat_result_list = qstat_result.split('\n')
            #创建一个大列表
            job_temp_list = []
            #去掉job id这行，添加到整个列表
            for i in qstat_result_list[1:]:
                job_temp_list.append(i.strip())
            #等于分割
            job_detal_list = []
            for i in job_temp_list:
                job_detal_list.append(i.split('='))
            job_start_time = ''
            job_run_time = ''
            #获取队列名称，用户名等等
            for i in range(len(job_detal_list)):
                if job_detal_list[i][0].strip() == 'Job_Name':
                    job_name = job_detal_list[i][1].strip()
                if job_detal_list[i][0].strip() == 'Job_Owner':
                    job_user_name = job_detal_list[i][1].strip().split('@')[0]
                if job_detal_list[i][0].strip() == 'queue':
                    job_queue = job_detal_list[i][1].strip()
                if job_detal_list[i][0].strip() == 'start_time':
                    job_start_time = job_detal_list[i][1].strip()
                if job_detal_list[i][0].strip() == 'resources_used.walltime':
                    job_run_time = job_detal_list[i][1].strip()
                    print job_run_time
                if job_detal_list[i][0].strip() == 'job_state':
                    job_status = job_detal_list[i][1].strip()
            data_insert = Job_list(job_id=job_id,job_name=job_name,job_user_name=job_user_name,
                                   job_queue=job_queue,job_start_time=job_start_time,job_run_time=job_run_time,
                                   job_status=job_status)
            data_insert.save()
            #return HttpResponse(data_insert)
        except Exception, e:
            print e
            #return HttpResponse(data_insert)
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
  
    return render_to_response('job/job_mgr.html')
   
