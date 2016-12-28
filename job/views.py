#coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from clusmgr.remote_help import curr_user_cmd
import commands
import time
from models import Job_list
from monitor.models import *
import csv
from config.config import *
import json
import time
import datetime
from job.job_help import create_job_help

def get_job_list(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    user_name = user_dict['user_name']
    result_list = []
    job_list_info = {}
    if req.method == 'POST':
        try:
            #查询处理
            search_user_name = req.POST.get('job_user_name', None)
            search_date_from = req.POST.get('date_from', None)
            search_date_to   = req.POST.get('date_to', None)
            search_sql = ''
            #排序,默认从id来排序
            sort_name = req.POST.get('sort','id')
            sort_order = req.POST.get('order','desc')
            #rows 每页显示多少条 
            #数据格式{'total':xx,'rows':[{r1:r1},{r2:r2}]}
            pageSize = int(req.POST.get('rows'))
            page = int(req.POST.get('page'))
            start = (page - 1)*pageSize
            #end = page*pageSize
            end = pageSize
            total = Job_list.objects.all().count()
            #qstat查询job信息，更新数据库字段
            #temp_result = Job_list.objects.exclude(job_status=['C','E','T'])
            if user_name == 'root':
                temp_result = Job_list.objects.raw("select * from job_job_list where job_status!='C' and \
                                                    job_status!='E' and job_status!='T' order by %s %s limit %s,%s"%(sort_name,sort_order,start,end))
            else:
                temp_result = Job_list.objects.raw("select * from job_job_list where job_status!='C' and \
                                                    job_status!='E' and job_status!='T' and job_user_name='%s' order by %s %s limit %s,%s"%(user_name,sort_name,sort_order,start,end))
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
                            job_start_time = datetime.datetime.strptime(job_start_time,"%a %b %d %H:%M:%S %Y")
                            row_data.update(job_start_time = job_start_time)
                        if job_detal_list[i][0].strip() == 'resources_used.walltime':
                            job_run_time = job_detal_list[i][1].strip()
                            job_run_time = datetime.datetime.strptime(job_run_time, "%H:%M:%S")  
                            row_data.update(job_run_time = job_run_time)
                        if job_detal_list[i][0].strip() == 'job_state':
                            job_status = job_detal_list[i][1].strip()
                            row_data.update(job_status = job_status)
            #get job info 
            #select job info in mysql            
            '''
            if sort_order == 'desc':
                sort_name = '-' + sort_name
            '''
            #判断查询用户名,python输出%需要用%%，django数据库查询也需要%%转义
            if search_user_name:
                search_sql = "job_user_name like '%%%%%s%%%%' and " %(search_user_name)
            if search_date_from:
                search_sql = "%s job_start_time >= '%s' and " %(search_sql,search_date_from)
            if search_date_to:
                search_sql = "%s job_start_time <= '%s' and " %(search_sql,search_date_to)
            
            #total = Job_list.objects.raw("select count(*) from job_job_list")
            if user_name == 'root':
                #all_result = Job_list.objects.all().order_by(sort_name)[start:end]
                if search_sql:
                    #添加where并去掉最后的and
                    search_sql = "where %s" %(search_sql[:-4])      
                all_result = Job_list.objects.raw("select * from job_job_list %s order by %s %s limit %s,%s"%(search_sql,sort_name,sort_order,start,end))
            else:
                #all_result = Job_list.objects.filter(job_user_name=user_name).order_by(sort_name)[start:end]
                all_result = Job_list.objects.raw("select * from job_job_list where %s job_user_name='%s' order by %s %s limit %s,%s" %(search_sql,user_name,sort_name,sort_order,start,end))
            job_status_dict = {'C':u'完成','E':u'退出','H':u'挂起','Q':u'排队','R':'运行','T':u'移动','W':u'排队','S':u'暂停'}
            for i in all_result:
                temp_dict={}
                temp_dict['job_id'] = i.job_id
                temp_dict['job_name'] = i.job_name
                temp_dict['job_user_name'] = i.job_user_name
                temp_dict['job_queue'] = i.job_queue
                temp_dict['job_start_time'] = i.job_start_time.strftime("%Y-%m-%d %H:%M:%S")
                temp_dict['job_run_time'] = i.job_run_time.strftime("%H:%M:%S")
                temp_dict['job_status'] = job_status_dict[i.job_status]
                result_list.append(temp_dict)
            if not result_list:
                result_list = [u'没有任何任务信息!！']
            job_list_info['total'] = total
            job_list_info['rows'] = result_list
            job_list_info = json.dumps(job_list_info)
            return HttpResponse(job_list_info)
        except Exception,e:
            #result_list = [u'没有任何任务信息！']
            result_list = [e]
            return HttpResponse(result_list)
    else:
        return HttpResponse('failed')

def mgr_job(req,page):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")    
    return render(req,'job/mgr_job.html')

def create_job_index(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    user_name = user_dict['user_name']
    #获取队列列表
    cmd = curr_user_cmd(user_name, QSTAT + '  -Q')
    queue_list = []
    queue_stats = commands.getstatusoutput(cmd)
    if not queue_stats[0]:
        temp_queue_stats = queue_stats[1].split('\n')[2:]
        for queue in temp_queue_stats:
            queue_name = queue.split()[0]
            queue_list.append(queue_name)
            
    else:
        queue_name = u'无法获取队列名'
        queue_list.append(queue_name)
    return render(req,'job/create_job.html',{'queue_data':queue_list})

def create_general_job(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if req.method == 'POST':
        if not user_dict:
            return HttpResponse("no data")
        user_name = user_dict['user_name']
        try:
            job_name = req.POST['general_job_name']
            work_dir = req.POST['general_workdir']
            queue_name = req.POST['general_queue_name']
            node_num = req.POST['general_node_num']
            core_num = req.POST['general_core_num']
            job_script = req.POST['general_jobscript']
            #cmd = req.POST['cmd']
            #pbs subcommit command

            #qsub_command = '%s -N %s -o %s -e %s -q %s -l nodes=%s:ppn=%s %s' %(QSUB,job_name,work_dir,work_dir,queue_name,node_num,core_num,job_script)
            #qsub_command = "echo " + "'" + UserInput['job_name'] + "'" + '|' + QSUB
            #命令行提交
            #qsub_command = "echo %s" %(cmd) + "|" + qsub_command
            #submit job
            qsub_command = curr_user_cmd(user_name, '%s -N %s -o %s -e %s -q %s -l nodes=%s:ppn=%s %s' \
                                                    %(QSUB,job_name,work_dir,work_dir,queue_name,node_num,core_num,job_script))
            qsub_submit_result = commands.getstatusoutput(qsub_command)
            if qsub_submit_result[0]:
                return HttpResponse(qsub_submit_result[1]) 
            create_job_result = create_job_help(qsub_submit_result, user_name)
            return HttpResponse(create_job_result)
        except Exception,e:
            return HttpResponse(e)
    else:
        return HttpResponse('no data')

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
        
        
def report_job_index(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login") 
    return render(req,'job/report_job_index.html')

def report_job(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login") 
    #生成csv文件
    response = HttpResponse(content_type='text/csv')
    curr_time = time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime())
    response['Content-Disposition'] = 'attachment; filename="report_job_%s.csv"'%curr_time
    writer = csv.writer(response)
    report_head = [u'作业ID',u'作业名称',u'用户名',u'队列',u'开始时间',u'运行时间',u'作业状态']
    writer.writerow([unicode(s).encode("gb2312") for s in report_head])
    job_status_dict = {'C':u'完成','E':u'退出','H':u'挂起','Q':u'排队','R':u'运行','T':u'移动','W':u'排队','S':u'暂停'}
    all_result = Job_list.objects.all().order_by("-id")
    for i in all_result:
        result_list = []
        result_list.append(i.job_id)
        result_list.append(i.job_name)
        result_list.append(i.job_user_name)
        result_list.append(i.job_queue)
        result_list.append(i.job_start_time)
        result_list.append(i.job_run_time)
        result_list.append(job_status_dict[i.job_status].encode('gb2312'))
        writer.writerow(result_list)
    return response