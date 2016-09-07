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

def get_net_info():
    #psutil.net_io_counters(pernic=True)['eth0'].bytes_sent
    # 'eth0': snetio(bytes_sent=19945156, bytes_recv=285446630, packets_sent=104032,
    # packets_recv=271597, errin=0, errout=0, dropin=2, dropout=0),
    #{'eth0':[ip,netmaks]}
    #{'eth0': {'nic_ip': '192.168.1.50', 'nic_bytes_sent': 19948716, 'nic_speed': 1000,
    #'nic_mask':'255.255.255.0', 'nic_bytes_recv': 286042697}}
    nics = psutil.net_io_counters(pernic=True)
    nic_dict = {}
    for nic_name in nics.keys():
        if nic_name != 'gif0' and nic_name != 'stf0':
            temp_dict = {}
            nic_ip = psutil.net_if_addrs()[nic_name][0].address
            nic_netmask = psutil.net_if_addrs()[nic_name][0].netmask
            nic_speed = psutil.net_if_stats()[nic_name].speed
            nic_bytes_sent = nics[nic_name].bytes_sent
            nic_bytes_recv = nics[nic_name].bytes_recv
            temp_dict['nic_ip'] = nic_ip
            temp_dict['nic_mask'] = nic_netmask
            temp_dict['nic_speed'] = nic_speed
            temp_dict['nic_bytes_sent'] = nic_bytes_sent
            temp_dict['nic_bytes_recv'] = nic_bytes_recv
            nic_dict[nic_name] = temp_dict
    return nic_dict

def urlPost(postdata):
    data = urllib.urlencode(postdata)
    req = urllib2.Request('http://127.0.0.1:8000/api/collect/',data)
    response = urllib2.urlopen(req)
    return response.read()

if __name__ == '__main__':
    while True:
        temp_dict = {}
        hostname = socket.gethostname()
        net_data = get_net_info()
        plugin_name = '#get_net_info'
        temp_dict[hostname+plugin_name] = net_data
        print temp_dict
        print urlPost(temp_dict)
        time.sleep(10)
