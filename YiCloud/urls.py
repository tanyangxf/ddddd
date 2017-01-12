"""YiCloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# -*- coding: utf-8 -*-
from django.conf.urls import url,include
from django.contrib.admin import site
from django.contrib import admin
from job.views import mgr_job,create_general_job,create_job_index,del_job,hold_job,stop_job,report_job,report_job_index,get_job_list
from monitor.monitor_api.monitor_server_api import monitor_collect
from sysmgr.views import host_mgr,get_host_list,create_host,user_mgr,get_user_list,del_user,del_host,modify_host,modify_user,create_user,\
                        node_tree,user_tree,host_power_mgr,get_host_power,host_power_index,storage_mgr,create_share_storage,del_share_storage,get_storage_list
from sysmgr.sysmgr_api.get_node import get_node_tree
from sysmgr.sysmgr_api.get_user import get_user_tree
from monitor.views import node_list,node_monitor,report_monitor_index,report_monitor_cpu,report_monitor_mem,\
                            report_monitor_net,report_monitor_disk,monitor_alarm_index,del_alarm
from index.views import default,login,index,logout,get_session
from clusmgr.views import dir_tree,file_tree,mgr_file,dir_content,mgr_dir_tree,mgr_process,vnc_login,file_upload,file_download
from clusmgr.clusmgr_api.tree_api import  get_dir_tree,get_file_tree
from schedmgr.views import mgr_sched_index,mgr_queue_index,get_sched_service,mgr_node_sched,mgr_sched_service,del_queue,get_queue_list,create_queue,mgr_user_sched,\
                            queue_tree,modify_user_sched
from schedmgr.schedmgr_api.queue_tree import get_queue_tree

urlpatterns = [
    url(r'^$',default, name='default'),
    url(r'^login/$',login, name='login'),
    url(r'^logout/$',logout, name='logout'),
    url(r'^index/$', index, name='index'),
    url(r'^get_session/$', get_session, name='get_session'),
    url(r'^schedmgr/mgr_queue_index/$', mgr_queue_index, name='mgr_queue_index'),
    url(r'^schedmgr/create_queue/$', create_queue, name='create_queue'),
    url(r'^schedmgr/get_queue_list/$', get_queue_list, name='get_queue_list'),
    url(r'^schedmgr/del_queue/$', del_queue, name='del_queue'),
    url(r'^schedmgr/mgr_node_sched/$', mgr_node_sched, name='mgr_node_sched'),
    url(r'^schedmgr/mgr_sched_index/$', mgr_sched_index, name='mgr_sched_index'),
    url(r'^schedmgr/mgr_sched_service/$', mgr_sched_service, name='mgr_sched_service'),
    url(r'^schedmgr/get_sched_service/$', get_sched_service, name='get_sched_service'),
    url(r'^schedmgr/mgr_user_sched/$', mgr_user_sched, name='mgr_user_sched'),
    url(r'^schedmgr/modify_user_sched/$', modify_user_sched, name='modify_user_sched'),
    url(r'^schedmgr/queue_tree/$', queue_tree, name='queue_tree'),
    url(r'^schedmgr_api/get_queue_tree/$',get_queue_tree,name='get_queue_tree'),
    url(r'^monitor_api/monitor_collect/$', monitor_collect, name='monitor_collect'),
    url(r'^sysmgr/host_mgr/',host_mgr,name='host_mgr'),
    url(r'^sysmgr/create_host/',create_host,name='create_host'),
    url(r'^sysmgr/get_host_list/',get_host_list,name='get_host_list'),
    url(r'^sysmgr/host_power_mgr/',host_power_mgr,name='host_power_mgr'),
    url(r'^sysmgr/host_power_index/$',host_power_index,name='host_power_index'),
    url(r'^sysmgr/get_host_power/$',get_host_power,name='get_host_power'),
    url(r'^sysmgr/user_mgr/',user_mgr,name='user_mgr'),
    url(r'^sysmgr/get_user_list/',get_user_list,name='get_user_list'),
    url(r'^sysmgr/create_user/$',create_user,name='create_user'),
    url(r'^sysmgr/del_user/$',del_user,name='del_user'),
    url(r'^sysmgr/modify_user/$',modify_user,name='modify_user'),
    url(r'^sysmgr/del_host/$',del_host,name='del_host'),
    url(r'^sysmgr/modify_host/$',modify_host,name='modify_host'),
    url(r'^sysmgr/node_tree/$',node_tree,name='node_tree'),
    url(r'^sysmgr/user_tree/$',user_tree,name='user_tree'),
    url(r'^sysmgr/storage_mgr/$',storage_mgr,name='storage_mgr'),
    url(r'^sysmgr/get_storage_list/$',get_storage_list,name='get_storage_list'),
    url(r'^sysmgr/create_share_storage/$',create_share_storage,name='create_share_storage'),
    url(r'^sysmgr/del_share_storage/$',del_share_storage,name='del_share_storage'),
    url(r'^sysmgr_api/get_node_tree/$',get_node_tree,name='get_node_tree'),
    url(r'^sysmgr_api/get_user_tree/$',get_user_tree,name='get_user_tree'),
    url(r'^job/create_job_index/$', create_job_index, name='create_job_index'),
    url(r'^job/create_general_job/$', create_general_job, name='create_general_job'),
    url(r'^job/mgr_job/', mgr_job, name='mgr_job'),
    url(r'^job/get_job_list/$',get_job_list,name='get_job_list'),  
    url(r'^job/del_job/$',del_job,name='del_job'),  
    url(r'^job/hold_job/$',hold_job,name='hold_job'), 
    url(r'^job/stop_job/$',stop_job,name='stop_job'), 
    url(r'^job/report_job_index/$',report_job_index,name='report_job_index'), 
    url(r'^job/report_job/$',report_job,name='report_job'), 
    url(r'^monitor/node_list/$',node_list,name='node_list'), 
    url(r'^monitor/node_monitor/$',node_monitor,name='node_monitor'), 
    url(r'^monitor/report_monitor_index/$',report_monitor_index,name='report_monitor_index'), 
    url(r'^monitor/report_monitor_cpu/$',report_monitor_cpu,name='report_monitor_cpu'), 
    url(r'^monitor/report_monitor_mem/$',report_monitor_mem,name='report_monitor_mem'), 
    url(r'^monitor/report_monitor_net/$',report_monitor_net,name='report_monitor_net'), 
    url(r'^monitor/report_monitor_disk/$',report_monitor_disk,name='report_monitor_disk'), 
    url(r'^monitor/monitor_alarm_index/(\d*)',monitor_alarm_index,name='monitor_alarm_index'),
    url(r'^monitor/del_alarm/$',del_alarm,name='del_alarm'),  
    url(r'^clusmgr/dir_tree/$',dir_tree,name='dir_tree'), 
    url(r'^clusmgr_api/get_dir_tree/$',get_dir_tree,name='get_dir_tree'), 
    url(r'^clusmgr/file_tree/$',file_tree,name='file_tree'), 
    url(r'^clusmgr/mgr_file/$',mgr_file,name='mgr_file'), 
    url(r'^clusmgr/dir_content/$',dir_content,name='dir_content'), 
    url(r'^clusmgr_api/get_file_tree/$',get_file_tree,name='get_file_tree'),
    url(r'^clusmgr/mgr_dir_tree/$',mgr_dir_tree,name='mgr_dir_tree'),
    url(r'^clusmgr/mgr_process/$',mgr_process,name='mgr_process'),
    url(r'^clusmgr/vnc_login/$',vnc_login,name='vnc_login'),
    url(r'^clusmgr/file_upload/$',file_upload,name='file_upload'),
    url(r'^clusmgr/file_download/$',file_download,name='file_download'),
]
