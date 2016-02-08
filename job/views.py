#coding=utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
import commands

from models import Job_list

# Create your views here.
def index(req):
    return render_to_response('index.html')

def new_job(req):
    if req.method == 'POST':
        try:
            userInput = req.POST
            print userInput
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
        #update job info in mysql
        #temp_result = Job_list.objects.exclude(job_status=['C','E','T'])
        temp_result = Job_list.objects.raw("select * from job_job_list where job_status!='C' and \
         job_status!='E' and job_status!='T'")
        for job_info in temp_result:
            qstat_command = "qstat -f %s" % job_info.job_id
            if qstat_command:
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
                row_data = Job_list.objects.get(job_id=job_info.job_id)
                #获取队列名称，用户名等等
                for i in range(len(job_detal_list)):
                    if job_detal_list[i][0].strip() == 'resources_used.walltime':
                        job_run_time = job_detal_list[i][1].strip()
                        row_data.job_run_time = job_run_time
                    if job_detal_list[i][0].strip() == 'job_state':
                        job_status = job_detal_list[i][1].strip()
                        row_data.job_status = job_status
                    row_data.save()
                
        #select job info in mysql
        all_result = Job_list.objects.all()
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
        return render_to_response('job/new_job.html',{'job_data':result_list})

def job_mgr(req):
  
    return render_to_response('job/job_mgr.html')

def cpu_monitor(req):
    data = [20,30,10,20,400]
    return render_to_response('job/cpu_monitor.html',{'data1':data[0],'data2':data[1],
                                                      'data3':data[2],'data4':data[3],
                                                      'data5':data[4]})

def mem_monitor(req):
    pass
   
def collect(req):
    if req.method == 'POST':
        data = req.POST
        #return render_to_response('job/job_mgr.html',{'cpu_count':p_cpu_count})
        hostname = data.keys()[0].split('.')[0]
        plugin_name = data.keys()[0].split('.')[1]
        monitor_data = eval(data.values()[0])
        if plugin_name == 'get_mem_info':
            mem_total = monitor_data['mem_total']
            mem_percent = monitor_data['mem_percent']
            swap_total = monitor_data['swap_total']
            swap_percent = monitor_data['swap_percent']
            print mem_total,mem_percent,swap_total,swap_percent
        elif plugin_name == 'get_cpu_info':
            pass
        elif plugin_name == 'get_net_info':
            pass
        elif plugin_name == 'get_disk_info':
            pass
        else:
            return HttpResponse('failed')
        return HttpResponse('ok')
    else:
        return render_to_response('index.html')
