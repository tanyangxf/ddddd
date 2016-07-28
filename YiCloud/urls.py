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
from job.views import new_job,index,job_mgr,cpu_monitor,mem_monitor
from monitor.api.monitor_server_api import collect
from sysmgr.views import host_mgr,login

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$',login, name='login'),
    url(r'^hpc/', index, name='index'),
    url(r'^job/new_job/(\d*)', new_job, name='new_job'),
    url(r'^job/job_mgr/$', job_mgr, name='job_mgr'),
    url(r'^job/cpu_monitor/$', cpu_monitor, name='cpu_monitor'),
    url(r'^job/mem_monitor/$', mem_monitor, name='mem_monitor'),
    url(r'^api/collect/$', collect, name='collect'),
    url(r'^sysmgr/host_mgr/(\d*)',host_mgr,name='host_mgr'),
]
