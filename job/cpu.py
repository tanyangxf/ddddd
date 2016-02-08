#!/usr/bin/env python
# encoding: utf-8
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

def get_mem_info():
    mem_dict = {}
    #unit M
    mem_total = psutil.virtual_memory().total/1024/1024
    mem_percent = psutil.virtual_memory().percent
    #mem_used = psutil.virtual_memory().used/1024/1024
    #mem_free = psutil.virtual_memory().free/1024/1024
    swap_total = psutil.swap_memory().total/1024/1024
    #swap_used = psutil.swap_memory().used/1024/1024
    #swap_free = psutil.swap_memory().free/1024/1024
    swap_percent = psutil.swap_memory().percent

    #add to mem_dict
    mem_dict['mem_total'] = mem_total
    mem_dict['mem_percent'] = mem_percent
    #mem_dict['mem_used'] = mem_used
    #mem_dict['mem_free'] = mem_free
    mem_dict['swap_total'] = swap_total
   #mem_dict['swap_used'] = swap_used
    #mem_dict['swap_free'] = swap_free
    mem_dict['swap_percent'] = swap_percent
    return mem_dict

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
    req = urllib2.Request('http://172.2.9.50:8000/job/collect/',data)
    response = urllib2.urlopen(req)
    return response.read()

if __name__ == '__main__':
    while True:
        temp_dict = {}
        hostname = socket.gethostname()
        mem_data = get_mem_info()
        plugin_name = '.get_mem_info'

        temp_dict[hostname+plugin_name] = mem_data

        print temp_dict
        urlPost(temp_dict)
        time.sleep(100)
