#coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from clusmgr.remote_help import curr_user_cmd
import commands
import time
import json
from models import Job_list
from monitor.models import *
PESTAT = '/usr/bin/pestat'
PBSNODES = '/torque2.4/bin/pbsnodes'
QSUB = '/torque2.4/bin/qsub'
QDEL= '/torque2.4/bin/qdel'
QSTAT = '/torque2.4/bin/qstat'
QHOLD = '/torque2.4/bin/qhold'

def mgr_job(req,page):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    user_name = user_dict['user_name']
    try:
        page = int(page)
    except Exception:
        page = 1
    #qstat查询job信息，更新数据库字段
    #temp_result = Job_list.objects.exclude(job_status=['C','E','T'])
    if user_name == 'root':
        temp_result = Job_list.objects.raw("select * from job_job_list where job_status!='C' and \
                                            job_status!='E' and job_status!='T'")
    else:
        temp_result = Job_list.objects.raw("select * from job_job_list where job_status!='C' and \
                                            job_status!='E' and job_status!='T' and job_user_name='%s'"%user_name)
    for job_info in temp_result:
        qstat_command = curr_user_cmd(user_name, QSTAT + " -f %s" % job_info.job_id)
        qstat_result = commands.getoutput(qstat_command)
        if qstat_result.startswith('qstat: Unknown'):
            row_data = Job_list.objects.filter(job_id=job_info.job_id)
            row_data.update(job_status='C')
        elif qstat_result.startswith('Job Id:'):
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
            row_data = Job_list.objects.filter(job_id=job_info.job_id)
            #获取队列名称，用户名等等
            for i in range(len(job_detal_list)):
                if job_detal_list[i][0].strip() == 'start_time':
                    job_start_time = job_detal_list[i][1].strip()
                    job_start_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                               time.strptime(job_start_time,"%a %b %d %H:%M:%S %Y"))
                    row_data.update(job_start_time = job_start_time)
                if job_detal_list[i][0].strip() == 'resources_used.walltime':
                    job_run_time = job_detal_list[i][1].strip()
                    row_data.update(job_run_time = job_run_time)
                if job_detal_list[i][0].strip() == 'job_state':
                    job_status = job_detal_list[i][1].strip()
                    row_data.update(job_status = job_status)
                        
    #从mysql中查找job数据
    #dispaly num per page    
    num = 5
    start = (page - 1)*num
    end = page*5
    if user_name == 'root':
        total = Job_list.objects.all().count()
        all_result = Job_list.objects.all().order_by("-id")[start:end]
    else:
        total = Job_list.objects.filter(job_user_name=user_name).count()
        all_result = Job_list.objects.filter(job_user_name=user_name).order_by("-id")[start:end]
    #divmod(14,5),result 2,4
    temp = divmod(total,num)
    if temp[1] == 0:
        all_page_count = temp[0]
    else:
        all_page_count = temp[0] + 1
        
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
        '''
    if all_result:
        temp_dict = {}
        temp_dict['msg'] = u'没有任何作业信息！'
        result_list.append(temp_dict)
        '''
    return render(req,'job/mgr_job.html',{'job_data':result_list,'all_page_count':range(all_page_count)})

def create_job(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if req.method == 'POST':
        if not user_dict:
            return HttpResponse("no data")
        user_name = user_dict['user_name']
        try:
            job_name = req.POST['job_name']
            work_dir = req.POST['work_dir']
            queue_name = req.POST['queue_name']
            node_num = req.POST['node_num']
            core_num = req.POST['core_num']
            job_script = req.POST['job_script']
            #cmd = req.POST['cmd']
            #pbs subcommit command

            #qsub_command = '%s -N %s -o %s -e %s -q %s -l nodes=%s:ppn=%s %s' %(QSUB,job_name,work_dir,work_dir,queue_name,node_num,core_num,job_script)
            #qsub_command = "echo " + "'" + UserInput['job_name'] + "'" + '|' + QSUB
            #命令行提交
            #qsub_command = "echo %s" %(cmd) + "|" + qsub_command
            #submit job
            qsub_command = curr_user_cmd(user_name, '%s -N %s -o %s -e %s -q %s -l nodes=%s:ppn=%s %s' \
                                                    %(QSUB,job_name,work_dir,work_dir,queue_name,node_num,core_num,job_script))
            qsub_submit = commands.getoutput(qsub_command)
            #get job_id
            job_id = qsub_submit.split('.')[0]
            #get job detal command
            #qstat_command = QSTAT + " -f %s" % job_id
            qstat_command =  curr_user_cmd(user_name,QSTAT + " -f %s" % job_id)
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
                    job_start_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                                   time.strptime(job_start_time,"%a %b %d %H:%M:%S %Y"))
                if job_detal_list[i][0].strip() == 'resources_used.walltime':
                    job_run_time = job_detal_list[i][1].strip()
                if job_detal_list[i][0].strip() == 'job_state':
                    job_status = job_detal_list[i][1].strip()
            data_insert = Job_list(job_id=job_id,job_name=job_name,job_user_name=job_user_name,
                                   job_queue=job_queue,job_start_time=job_start_time,job_run_time=job_run_time,
                                   job_status=job_status)
            data_insert.save()
            return HttpResponse('ok')
        except Exception:
            return HttpResponse('failed')
    else:
        if not user_dict:
            return redirect("/login")
        user_name = user_dict['user_name']
        #获取队列列表
        cmd = curr_user_cmd(user_name, QSTAT + '  -Q')
        queue_list = []
        queue_stats = commands.getoutput(cmd)
        temp_queue_stats = queue_stats.split('\n')[2:]
        for queue in temp_queue_stats:
            queue_name = queue.split()[0]
            queue_list.append(queue_name)
        return render(req,'job/create_job.html',{'queue_data':queue_list})

def del_job(req): 
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    user_name = user_dict['user_name']
    if req.method == 'POST':
        job_id = req.POST.get('job_id',None)  
        if job_id:                      
            for job_id in job_id.split(','):               
                job_id = int(job_id)
                qdel_command = curr_user_cmd(user_name, QDEL + '  %d' %job_id)
                commands.getstatusoutput(qdel_command)
                try:
                    del_data = Job_list.objects.filter(job_id=job_id)
                    del_data.delete()
                except:
                    return HttpResponse('failed')
            return HttpResponse('ok')
        else:
            return HttpResponse('failed')

def hold_job(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login") 
    user_name = user_dict['user_name']
    if req.method == 'POST':
        job_id = req.POST.get('job_id',None)             
        if job_id:                      
            for job_id in job_id.split(','):               
                job_id = int(job_id)
                qhold_command = curr_user_cmd(user_name, QHOLD + '  %d' %job_id   )
                qhold_command_result = commands.getstatusoutput(qhold_command)
                if qhold_command_result[0] > 0:
                    return HttpResponse('failed')
            return HttpResponse('ok')
        else:
            return HttpResponse('failed')
def stop_job(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login") 
    user_name = user_dict['user_name']
    if req.method == 'POST':
        job_id = req.POST.get('job_id',None)             
        if job_id:                      
            for job_id in job_id.split(','):               
                job_id = int(job_id)
                qstop_command = curr_user_cmd(user_name, QDEL + '  %d' %job_id )
                qstop_command_result = commands.getstatusoutput(qstop_command)
                if qstop_command_result[0] > 0:
                    return HttpResponse('failed')
                return HttpResponse('ok')
                
        else:
            return HttpResponse('failed')
        