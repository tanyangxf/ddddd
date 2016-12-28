#coding=utf-8
from config.config import *
import commands
from django.http import HttpResponse
from clusmgr.remote_help import curr_user_cmd
import datetime
from models import Job_list

def create_job_help(qsub_submit_result,user_name):
    #get job_id
    #if qsub_submit is ok
    try:
        qsub_submit_result = qsub_submit_result[1]
        job_id = qsub_submit_result.split('.')[0]
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
        job_run_time = '00:00:00'
        #获取队列名称，用户名等等
        for i in range(len(job_detal_list)):
            if job_detal_list[i][0].strip() == 'Job_Name':
                job_name = job_detal_list[i][1].strip()
            if job_detal_list[i][0].strip() == 'Job_Owner':
                job_user_name = job_detal_list[i][1].strip().split('@')[0]
            if job_detal_list[i][0].strip() == 'queue':
                job_queue = job_detal_list[i][1].strip()
            if job_detal_list[i][0].strip() == 'ctime':
                job_start_time = job_detal_list[i][1].strip()
                job_start_time = datetime.datetime.strptime(job_start_time,"%a %b %d %H:%M:%S %Y")
            if job_detal_list[i][0].strip() == 'resources_used.walltime':
                job_run_time = job_detal_list[i][1].strip()
                job_run_time = datetime.datetime.strptime(job_run_time, "%H:%M:%S")  
            if job_detal_list[i][0].strip() == 'job_state':
                job_status = job_detal_list[i][1].strip()
        print job_id,job_name,job_user_name,job_start_time
        data_insert = Job_list(job_id=job_id,job_name=job_name,job_user_name=job_user_name,
                               job_queue=job_queue,job_start_time=job_start_time,job_run_time=job_run_time,
                               job_status=job_status)
        data_insert.save()
        return u'作业id:  ' + job_id + ' ' + u'提交成功'
    except Exception,e:
        return e
