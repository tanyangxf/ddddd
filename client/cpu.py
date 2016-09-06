#!/usr/bin/env python
# encoding: utf-8
'''
Created on 2016年9月6日

@author: tanyang
'''
import urllib, urllib2
import psutil
import time
import socket


def get_cpu_info():
    cpu_dict = {}
    l_cpu_count = psutil.cpu_count()
    #p_cpu_count = psutil.cpu_count(logical=False)
    #cpu_percent is a list [0.1,0.3]
    #cpu_percent = psutil.cpu_percent(percpu=True)
    cpu_percent = psutil.cpu_percent(interval=0.1)
    #scputimes(user=0.2, nice=0.0, system=0.7, idle=99.0, iowait=0.0, irq=0.0, softirq=0.0,steal=0.0, guest=0.0, guest_nice=0.0)
    '''
    temp_cpu_info = psutil.cpu_times_percent(interval=0.01)
    cpu_percent_user = temp_cpu_info.user
    cpu_percent_nice = temp_cpu_info.nice
    cpu_percent_system = temp_cpu_info.system
    cpu_percent_idle = temp_cpu_info.idle
    cpu_percent_iowait = temp_cpu_info.iowait
    ''' 
    #add to dict
    cpu_dict['l_cpu_count'] = l_cpu_count
    #cpu_dict['p_cpu_count'] = p_cpu_count
    cpu_dict['cpu_percent'] = cpu_percent
    '''
    cpu_dict['cpu_percent_user'] = cpu_percent_user
    cpu_dict['cpu_percent_nice'] =  cpu_percent_nice
    cpu_dict['cpu_percent_system'] = cpu_percent_system
    cpu_dict['cpu_percent_idle'] = cpu_percent_idle
    cpu_dict['cpu_percent_iowait'] = cpu_percent_iowait
    '''
    return cpu_dict

def urlPost(postdata):
    data = urllib.urlencode(postdata)
    req = urllib2.Request('http://127.0.0.1:8000/api/collect/',data)
    response = urllib2.urlopen(req)
    return response.read()

if __name__ == '__main__':
    while True:
        temp_dict = {}
        hostname = socket.gethostname()
        cpu_data = get_cpu_info()
        plugin_name = '#get_cpu_info'
        temp_dict[hostname+plugin_name] = cpu_data
        print temp_dict
        urlPost(temp_dict)
        time.sleep(10)
