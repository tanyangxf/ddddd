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

def get_mem_info():
    mem_dict = {}
    #unit M
    mem_total = str(psutil.virtual_memory().total/1024/1024)
    mem_percent = str(psutil.virtual_memory().percent)
    mem_used = str(psutil.virtual_memory().used/1024/1024)
    #mem_free = psutil.virtual_memory().free/1024/1024
    swap_total = str(psutil.swap_memory().total/1024/1024)
    swap_used = str(psutil.swap_memory().used/1024/1024)
    #swap_free = psutil.swap_memory().free/1024/1024
    swap_percent = str(psutil.swap_memory().percent)

    #add to mem_dict
    mem_dict['mem_total'] = mem_total
    mem_dict['mem_percent'] = mem_percent
    mem_dict['mem_used'] = mem_used
    #mem_dict['mem_free'] = mem_free
    mem_dict['swap_total'] = swap_total
    mem_dict['swap_used'] = swap_used
    #mem_dict['swap_free'] = swap_free
    mem_dict['swap_percent'] = swap_percent
    return mem_dict

def urlPost(postdata):
    data = urllib.urlencode(postdata)
    req = urllib2.Request('http://172.16.123.140/monitor_api/monitor_collect/',data)
    response = urllib2.urlopen(req)
    return response.read()

if __name__ == '__main__':
    while True:
        temp_dict = {}
        hostname = socket.gethostname()
        mem_data = get_mem_info()
        plugin_name = '#get_mem_info'
        temp_dict[hostname+plugin_name] = mem_data
        print temp_dict
        print urlPost(temp_dict)
        time.sleep(10)
