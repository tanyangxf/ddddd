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

def get_disk_info():
    #[sdiskpart(device='/dev/sda5', mountpoint='/', fstype='ext4', opts='rw,errors=remount-ro')]
    disk_partitions = psutil.disk_partitions()
    #psutil.disk_usage('/')[0]
    #sdiskusage(total=40123162624, used=12292149248, free=25769250816, percent=32.3)
    disk_dict = {}
    for i in range(len(disk_partitions)):
        temp_dict = {}
        disk_name = disk_partitions[i].device
        disk_mountpoint = disk_partitions[i].mountpoint
        disk_total = psutil.disk_usage(disk_mountpoint).total/1024/1024/1024
        disk_percent = psutil.disk_usage(disk_mountpoint).percent
        temp_dict['disk_name'] = disk_name
        temp_dict['disk_total'] = disk_total
        temp_dict['disk_percent'] = disk_percent
        disk_dict[disk_mountpoint] = temp_dict
    return disk_dict


def urlPost(postdata):
    data = urllib.urlencode(postdata)
    req = urllib2.Request('http://127.0.0.1:8000/monitor_api/monitor_collect/',data)
    response = urllib2.urlopen(req)
    return response.read()

if __name__ == '__main__':
    while True:
        temp_dict = {}
        hostname = socket.gethostname()
        disk_data = get_disk_info()
        plugin_name = '#get_disk_info'
        temp_dict[hostname+plugin_name] = disk_data
        print temp_dict
        print urlPost(temp_dict)
        time.sleep(10)
