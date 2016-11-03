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
from django.conf.urls import url,include
from django.contrib.admin import site
from django.contrib import admin
from job.views import mgr_job,create_job,del_job,hold_job,stop_job
from monitor.monitor_api.monitor_server_api import monitor_collect
from sysmgr.views import host_mgr,user_mgr,del_user,del_host,modify_host,modify_user,create_user
from monitor.views import node_list,node_monitor
from index.views import default,login,index
from clusmgr.views import dir_tree,file_tree,mgr_file,dir_content,mgr_dir_tree,mgr_process,vnc_login
from clusmgr.clusmgr_api.tree_api import  get_dir_tree,get_file_tree
from schedmgr.views import mgr_queue,mgr_node_sched,mgr_sched_service

urlpatterns = [
    url(r'^$',default, name='default'),
    url(r'^login/$',login, name='login'),
    url(r'^index/$', index, name='index'),
    url(r'^job/create_job/$', create_job, name='create_job'),
    url(r'^job/mgr_job/(\d*)', mgr_job, name='mgr_job'),
    url(r'^schedmgr/mgr_queue/$', mgr_queue, name='mgr_queue'),
    url(r'^schedmgr/mgr_node_sched/$', mgr_node_sched, name='mgr_node_sched'),
    url(r'^schedmgr/mgr_sched_service/$', mgr_sched_service, name='mgr_sched_service'),
    url(r'^monitor_api/monitor_collect/$', monitor_collect, name='monitor_collect'),
    url(r'^sysmgr/host_mgr/(\d*)',host_mgr,name='host_mgr'),
    url(r'^sysmgr/user_mgr/(\d*)',user_mgr,name='user_mgr'),
    url(r'^sysmgr/create_user/$',create_user,name='create_user'),
    url(r'^sysmgr/del_user/$',del_user,name='del_user'),
    url(r'^sysmgr/modify_user/$',modify_user,name='modify_user'),
    url(r'^sysmgr/del_host/$',del_host,name='del_host'),
    url(r'^sysmgr/modify_host/$',modify_host,name='modify_host'),
    url(r'^job/del_job/$',del_job,name='del_job'),  
    url(r'^job/hold_job/$',hold_job,name='hold_job'), 
    url(r'^job/stop_job/$',stop_job,name='stop_job'), 
    url(r'^monitor/node_list/$',node_list,name='node_list'), 
    url(r'^monitor/node_monitor/$',node_monitor,name='node_monitor'), 
    url(r'^clusmgr/dir_tree/$',dir_tree,name='dir_tree'), 
    url(r'^clusmgr_api/get_dir_tree/$',get_dir_tree,name='get_dir_tree'), 
    url(r'^clusmgr/file_tree/$',file_tree,name='file_tree'), 
    url(r'^clusmgr/mgr_file/$',mgr_file,name='mgr_file'), 
    url(r'^clusmgr/dir_content/$',dir_content,name='dir_content'), 
    url(r'^clusmgr_api/get_file_tree/$',get_file_tree,name='get_file_tree'),
    url(r'^clusmgr/mgr_dir_tree/$',mgr_dir_tree,name='mgr_dir_tree'),
    url(r'^clusmgr/mgr_process/$',mgr_process,name='mgr_process'),
    url(r'^clusmgr/vnc_login/$',vnc_login,name='vnc_login'),
]
