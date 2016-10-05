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
from job.views import create_job,mgr_job,cpu_monitor,mem_monitor,del_job,hold_job,stop_job
from monitor.api.monitor_server_api import collect
from sysmgr.views import host_mgr,user_mgr,del_user,del_host,modify_host,modify_user
from monitor.views import node_monitor
from index.views import default,login,index

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$',default, name='default'),
    url(r'^login/$',login, name='login'),
    url(r'^index/$', index, name='index'),
    url(r'^job/create_job/(\d*)', create_job, name='create_job'),
    url(r'^job/job_mgr/$', mgr_job, name='mgr_job'),
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
