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
from django.conf.urls import include, url
from django.contrib import admin
from job.views import new_job,index,job_mgr,cpu_monitor,mem_monitor,del_job,hold_job,stop_job
from monitor.api.monitor_server_api import collect
from sysmgr.views import host_mgr,login,user_mgr,del_user,del_host,modify_host,modify_user
from monitor.views import node_monitor

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$',login, name='login'),
    url(r'^hpc/$', index, name='index'),
    url(r'^job/new_job/(\d*)', new_job, name='new_job'),
    url(r'^job/job_mgr/$', job_mgr, name='job_mgr'),
    url(r'^job/cpu_monitor/$', cpu_monitor, name='cpu_monitor'),
    url(r'^job/mem_monitor/$', mem_monitor, name='mem_monitor'),
    url(r'^api/collect/$', collect, name='collect'),
    url(r'^sysmgr/host_mgr/(\d*)',host_mgr,name='host_mgr'),
    url(r'^sysmgr/user_mgr/(\d*)',user_mgr,name='user_mgr'),
    url(r'^sysmgr/del_user/$',del_user,name='del_user'),
    url(r'^sysmgr/modify_user/$',modify_user,name='modify_user'),
    url(r'^sysmgr/del_host/$',del_host,name='del_host'),
    url(r'^sysmgr/modify_host/$',modify_host,name='modify_host'),
    url(r'^job/del_job/$',del_job,name='del_job'),  
    url(r'^job/hold_job/$',hold_job,name='hold_job'), 
    url(r'^job/stop_job/$',stop_job,name='stop_job'), 
    url(r'^monitor/node_monitor/$',node_monitor,name='node_monitor'), 
]
