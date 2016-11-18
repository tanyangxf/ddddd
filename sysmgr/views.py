#coding:utf-8
from django.shortcuts import render,HttpResponse
from monitor.models import Host
from django.shortcuts import redirect
from sysmgr.models import User
import commands
import crypt
import os
import string
import random
import subprocess
import socket
from clusmgr.remote_help import connect,exec_commands
from sysmgr.models import Storage
from django.db.models.query_utils import Q
import json
SHADOW_FILE = '/etc/shadow'
PASSWD_FILE = '/etc/passwd'
GROUP_FILE  = '/etc/group'
PBSNODES = '/torque2.4/bin/pbsnodes'
SOFT_SHUT = 'shutdown -h now'
SOFT_REBOOT = 'shutdown -r now'
NFS_SHARE_FILE = '/etc/exports'
NFS_TMP_FILE = '/tmp/exports'
NFS_SHOWMOUNT = 'showmount -e'

'''
ipmitool -I lan -H 10.1.199.212 -U ADMIN -P ADMIN chassis power off  
ipmitool -I lan -H 10.1.199.212 -U ADMIN -P ADMIN chassis power reset 
ipmitool -I lan -H 10.1.199.212 -U ADMIN -P ADMIN chassis power on   
ipmitool -I lan -H 10.1.199.212 -U ADMIN -P ADMIN chassis power status
'''

def node_tree(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    return render(req,'sysmgr/node_tree.html')

def user_tree(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    return render(req,'sysmgr/user_tree.html')

def host_mgr(req,page):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse('failed')
    try:
        page = int(page)
    except Exception:
        page = 1
    if req.method == 'POST':
        UserInput = req.POST
        host_name = UserInput['host_name']
        host_ip = UserInput['host_ip']
        host_ipmi = UserInput['host_ipmi']
        if host_name and host_ip:   
            data_insert = Host(host_name=host_name,host_ip=host_ip,host_ipmi=host_ipmi)
            data_insert.save()
            return HttpResponse('ok')
        else:
            return HttpResponse('failed')
    else:
        num = 12
        start = (page - 1)*num
        end = page*12
        total = Host.objects.all().count()
        all_result = Host.objects.all()[start:end]
        #divmod(14,5),result 2,4
        temp = divmod(total,num)
        if temp[1] == 0:
            all_page_count = temp[0]
        else:
            all_page_count = temp[0] + 1
        result_list = []
        for i in all_result:
            temp_dict = {}
            temp_dict['host_id'] = i.id
            temp_dict['host_name'] = i.host_name
            temp_dict['host_ip'] = i.host_ip
            temp_dict['host_ipmi'] = i.host_ipmi
            result_list.append(temp_dict)
        return render(req,'sysmgr/host_mgr.html',{'host_data':result_list,'all_page_count':range(all_page_count)})


def user_mgr(req,page):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse('failed')
    try:
        page = int(page)
    except Exception:
        page = 1
    user_name_list = []
    #查询用户列表中id大于500的用户，如果不在用户列表，插入数据库
    with open(PASSWD_FILE) as pwd_file:
        #循环passwd文件中的每一行，
        for user_info in pwd_file.readlines():
            user_name = user_info.split(":",1)[0]
            user_name_list.append(user_name)
            userid = int(user_info.split(":",3)[2])
            if userid > 500 and userid < 5000:
                db_user = User.objects.filter(user_name=user_name).values('user_name')
                #如果用户在数据库中不存在，插入数据库
                if not db_user:
                    user_home = user_info.split(":",6)[5]
                    user_shell = user_info.split(":")[-1].split('/')[-1]
                    group_result = commands.getoutput('id -Gn %s'%user_name).split(' ',1)
                    user_group = group_result[0]
                    if len(group_result) == 1:
                        other_group = ''
                    else:
                        other_group = group_result[1]
                    is_login = 'True'
                    user_type = u'普通用户'
                    user_mail = ''
                    user_tel = ''
                    user_comment = ''
                    #查询用户密码
                    with open(SHADOW_FILE) as shadow_file:
                        for src in shadow_file.readlines():
                            shadow_user = src.split(':',1)[0]
                            if user_name == shadow_user:
                                password = src.split(':',2)[1]
                                if password == '!!' or user_shell.strip() == 'nologin': #用户是否能登录
                                    is_login = 'False'
                                elif password.startswith("!") and len(password) > 2 : #用户是否能登录
                                    is_login = 'False'
                    data_insert = User(user_name=user_name,userid=userid,password=password,user_home=user_home,
                                       user_group=user_group,other_group=other_group,user_type=user_type,user_mail=user_mail,user_tel=user_tel,
                                       user_comment=user_comment,is_login=is_login)
                    data_insert.save()
                #如果在数据库中存在，查询密码是否和数据库中一致
                else:
                    with open(SHADOW_FILE) as shadow_file:
                        for src in shadow_file.readlines():
                            shadow_user = src.split(':',1)[0]
                            #判断数据库用户和操作系统用户 ，对比密码
                            if db_user[0]['user_name'] == shadow_user:
                                #判断该用户的操作系统密码是否有问题
                                osuser_password = src.split(':',2)[1]
                                db_pass = User.objects.filter(user_name=user_name).values('password')
                                if db_pass[0]['password'] != osuser_password:
                                    #更新数据库中的密码，以防被更改
                                    data_update = User.objects.get(user_name=shadow_user)
                                    data_update.password = osuser_password
                                    data_update.save()
    #判断数据库中存在的用户在系统是否存在
    db_user = User.objects.values('user_name')
    for user in db_user:
        user_name = user.values()[0].strip()
        if user_name != 'superuser' and user_name not in user_name_list:
            del_data = User.objects.get(user_name=user_name)
            del_data.delete()
    num = 5
    start = (page - 1)*num
    end = page*5
    total = User.objects.all().count()
    all_result = User.objects.all()[start:end]
    #divmod(14,5),result 2,4
    temp = divmod(total,num)
    if temp[1] == 0:
        all_page_count = temp[0]
    else:
        all_page_count = temp[0] + 1
    result_list = []
    for i in all_result:
        temp_dict = {}
        temp_dict['userid'] = i.userid
        temp_dict['user_name'] = i.user_name
        temp_dict['user_home'] = i.user_home
        temp_dict['user_group'] = i.user_group
        temp_dict['other_group'] = i.other_group
        temp_dict['user_type'] = i.user_type
        temp_dict['user_mail'] = i.user_mail
        temp_dict['user_tel'] = i.user_tel
        temp_dict['user_comment'] = i.user_comment
        temp_dict['is_login'] = i.is_login
        result_list.append(temp_dict)
    return render(req,'sysmgr/user_mgr.html',{'user_data':result_list,'all_page_count':range(all_page_count)})

def create_user(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    if req.method == 'POST':
        user_name = user_dict['user_name']
        if user_name != 'root':
            return HttpResponse('failed')
        user_name    = req.POST.get('user_name',None)
        password     = req.POST.get('password',None)
        user_home    = req.POST.get('user_home',None)
        user_group   = req.POST.get('user_group',None)
        other_group  = req.POST.get('other_group',None)
        is_login     = req.POST.get('is_login',None)
        user_type    = req.POST.get('user_type',None)
        user_mail    = req.POST.get('user_mail',None)
        user_tel     = req.POST.get('user_tel',None)
        user_comment = req.POST.get('user_comment',None)
        salt         = '$6$' + ''.join(random.sample(string.ascii_letters + string.digits, 8))
        encPass      = crypt.crypt(password,salt)
        try:   
            os.system("useradd -p \'"+encPass + "\' -d "+ user_home + " -G " + other_group + \
                  " -m "+ " -c \""+ user_comment+"\" " + user_name)
        except Exception:
            HttpResponse('failed')
        userid = int(commands.getoutput('id -u %s' %user_name))
        data_insert = User(user_name=user_name,userid=userid,password=encPass,user_home=user_home,user_group=user_group,
                           other_group=other_group,user_type=user_type,user_mail=user_mail,user_tel=user_tel,
                           user_comment=user_comment,is_login=is_login)
        data_insert.save()
        return HttpResponse('ok')
    else:
        return HttpResponse('failed')

def del_user(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse('failed')
    if req.method == 'POST':
        user_name = req.POST.get('user_name',None)
        if user_name:
            for user_name in user_name.split(','):
                commands.getoutput('userdel -r %s'%user_name)
                del_data = User.objects.get(user_name=user_name)
                del_data.delete()
            return HttpResponse('ok')
        else:
            return HttpResponse('failed!')

def modify_user(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse('failed')
    if req.method == 'POST':
        user_name = req.POST.get('user_name',None)
        user_pass = req.POST.get('user_pass',None)
        #user_home    = req.POST.get('user_home',None)
        user_group   = req.POST.get('user_group',None)
        other_group  = req.POST.get('other_group',None)
        is_login     = req.POST.get('is_login',None)
        #user_type    = req.POST.get('user_type',None)
        user_mail    = req.POST.get('user_mail',None)
        user_tel     = req.POST.get('user_tel',None)
        user_comment = req.POST.get('user_comment',None)
        userid = int(commands.getoutput('id -u %s' %user_name))
        user_data = User.objects.filter(userid=userid)
        if user_name == 'superuser':
            is_login = 'True'
        try:
            #如果密码没有修改  
            if user_pass != u'原始密码': 
                salt         = '$6$' + ''.join(random.sample(string.ascii_letters + string.digits, 8))
                encPass      = crypt.crypt(user_pass,salt)
                os.system("usermod -p \'"+encPass + "\'" + " -g " + user_group  + " -G " + other_group + \
                         " -c \""+ user_comment+"\" " + user_name)
                user_data.update(password = encPass)
            else:
                os.system("usermod"+ " -g " + user_group  + " -G " + other_group + \
                         " -c \""+ user_comment+"\"  " + user_name)
                print "usermod"+ " -g " + user_group  + " -G " + other_group + \
                         " -c \""+ user_comment+"\"  " + user_name
            user_data.update(user_group = user_group)
            user_data.update(other_group = other_group)
            user_data.update(is_login = is_login)
            user_data.update(user_tel = user_tel)
            user_data.update(user_mail = user_mail)
            user_data.update(user_comment = user_comment)
            return HttpResponse('ok')
        except Exception,e:
            print e
            HttpResponse('failed')
    else:
        return HttpResponse('not change!')

def del_host(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse('failed')
    if req.method == 'POST':
        host_num = req.POST.get('host_num',None)
        if host_num:
            for host_num in host_num.split(','):
                del_data = Host.objects.get(id=host_num)
                del_data.delete()
            return HttpResponse('ok')
        else:
            return HttpResponse('failed')
        
def modify_host(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse('failed')
    if req.method == 'POST':
        host_id = req.POST.get('host_id',None)
        host_name = req.POST.get('host_name',None)
        host_ip = req.POST.get('host_ip',None)
        host_ipmi = req.POST.get('host_ipmi',None)
        if host_name and host_ip: 
            row_data = Host.objects.filter(id=host_id)
            row_data.update(host_name = host_name)
            row_data.update(host_ip = host_ip)
            row_data.update(host_ipmi = host_ipmi)
            return HttpResponse('ok')
    else:
        return HttpResponse('not change!')


def host_power_mgr(req,page):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse('failed')
    try:
        page = int(page)
    except Exception:
        page = 1
    num = 12
    start = (page - 1)*num
    end = page*12
    total = Host.objects.all().count()
    all_result = Host.objects.all()[start:end]
    #divmod(14,5),result 2,4
    temp = divmod(total,num)
    if temp[1] == 0:
        all_page_count = temp[0]
    else:
        all_page_count = temp[0] + 1
    result_list = []
    for i in all_result:
        temp_dict = {}
        pbsnodes_result = commands.getstatusoutput(PBSNODES + ' -l down %s'%i.host_name)
        #pbsnodes_result 为0正确执行，如果不为0，pbs未安装，数据库确已配置
        if pbsnodes_result[0]:
            fnull = open(os.devnull, 'w')
            return1 = subprocess.call('ping %s -c  1'%i.host_name, shell = True, stdout = fnull, stderr = fnull)
            if return1:
                temp_dict['power_status'] = 'DOWN'
            else:
                temp_dict['power_status'] = 'OK'
            fnull.close()
        #pbsnodes正确执行，然后判断命令是否有返回，如果没有返回，pbs down，监测网络连通
        elif not pbsnodes_result[0] and not pbsnodes_result[1]:
            fnull = open(os.devnull, 'w')
            return1 = subprocess.call('ping %s -c 1'%i.host_name, shell = True, stdout = fnull, stderr = fnull)
            if return1:
                temp_dict['power_status'] = 'DOWN'
            else:
                temp_dict['power_status'] = 'OK'
            fnull.close()
        else:
            temp_dict['power_status'] = 'DOWN'
        temp_dict['host_name'] = i.host_name
        temp_dict['host_ip'] = i.host_ip
        temp_dict['host_ipmi'] = i.host_ipmi
        result_list.append(temp_dict)
    return render(req,'sysmgr/host_power_mgr.html',{'host_data':result_list,'all_page_count':range(all_page_count)})

def host_power(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return HttpResponse('failed')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse('failed')
    if req.method == 'POST':
        power_change = req.POST.get('power_change', None)
        host_name = req.POST.get('host_name', None)
        if power_change == 'soft_shut':
            exec_commands(connect(host_name,user_name),SOFT_SHUT)
        elif power_change == 'soft_reboot':
            exec_commands(connect(host_name,user_name),SOFT_REBOOT)
        elif power_change == 'hard_shut':
            pass
        elif power_change == 'hard_reboot':
            pass
        return HttpResponse('ok')
    return HttpResponse('no data')


def storage_mgr(req):
    req.session.set_expiry(1800)
    if req.method == 'POST':
        #点击获取共享详细信息
        folder_id = req.POST.get('folder_id',None)
        if folder_id:
            try:
                row_data = Storage.objects.get(id=folder_id)
                share_dict = {}
                share_dict['folder_name'] = row_data.folder_name
                share_dict['share_type'] = row_data.share_type
                share_dict['share_host'] = row_data.share_host
                share_dict['share_parameter'] = row_data.share_parameter
                share_dict['share_permission'] = row_data.share_permission
                share_dict['allow_ip'] = row_data.allow_ip
                share_dict = json.dumps(share_dict)
                return HttpResponse(share_dict)
            except:
                return HttpResponse('failed')
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name != 'root':
        return HttpResponse('failed')
    #获取数据库中所有值
    row_data = Storage.objects.all()
    share_dict = {}
    share_detail_dict = {}
    #记录id是唯一值
    for share_data in row_data:
        share_detail_dict[share_data.folder_name] = share_data.id
        share_dict[share_data.share_host] = share_detail_dict
    return render(req,'sysmgr/storage_mgr.html',{'share_dict':share_dict})

def create_share_storage(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if req.method == 'POST':
        user_name = user_dict['user_name']
        if user_name != 'root':
            return HttpResponse('failed')
        folder_name = req.POST.get('folder_name',None)
        share_type = req.POST.get('share_type',None)
        share_host    = req.POST.get('share_host',None)
        share_parameter   = req.POST.get('share_parameter',None)
        share_permission  = req.POST.get('share_permission',None)
        allow_ip  = req.POST.get('allow_ip',None)
        #如果没指定主机，默认为本机共享
        if not share_host:
            commands.getoutput('rm -f %s'%(NFS_TMP_FILE))
            commands.getoutput('cp %s %s'%(NFS_SHARE_FILE,NFS_TMP_FILE))
            #如果共享主机不存在，获取本机主机名
            share_host = socket.gethostname()
        else:
            commands.getoutput('rm -f %s'%(NFS_TMP_FILE))
            commands.getoutput('scp %s:%s %s'%(share_host,NFS_SHARE_FILE,NFS_TMP_FILE))
        sharefile_is_exsits = False
        with open(NFS_TMP_FILE,'r') as r:
            file_lines=r.readlines()
        with open(NFS_TMP_FILE,'w') as w:     
            for l in file_lines:
                #如果存在就修改
                if l.strip() and l.strip().split()[0] == folder_name:
                    sharefile_is_exsits = True
                    index_num = file_lines.index(l)
                    share_result = ''
                    for ip_add in allow_ip.split(','):
                        share_result = share_result + ' ' +  ip_add + '(' + share_permission + ',' + share_parameter + ')'
                    file_lines[index_num] =  folder_name + ' ' + share_result + '\n'
                    w.write(file_lines[index_num])
                    #判断在数据库中是否存在，如果存在，修改，不存在插入
                    row_data = Storage.objects.filter(folder_name=folder_name)
                    if row_data:
                        row_data.update(share_type = share_type)
                        row_data.update(share_parameter = share_parameter)
                        row_data.update(allow_ip = allow_ip)
                        row_data.update(share_permission = share_permission)
                        row_data.update(share_host = share_host)
                    else:
                        data_insert = Storage(folder_name=folder_name,share_type=share_type,share_parameter=share_parameter,
                                       allow_ip=allow_ip,share_permission=share_permission,share_host=share_host)
                        data_insert.save()
                else:
                    w.write(l) 
            #如果不存在就添加
            if not sharefile_is_exsits:
                share_result = ''
                for ip_add in allow_ip.split(','):
                    share_result = share_result + ' ' +  ip_add + '(' + share_permission + ',' + share_parameter + ')'
                add_lines =  folder_name + ' ' + share_result + '\n'
                w.write(add_lines)
                row_data = Storage.objects.filter(folder_name=folder_name)
                if row_data:
                    row_data.update(share_type = share_type)
                    row_data.update(share_parameter = share_parameter)
                    row_data.update(allow_ip = allow_ip)
                    row_data.update(share_permission = share_permission)
                    row_data.update(share_host = share_host)
                else:
                    data_insert = Storage(folder_name=folder_name,share_type=share_type,share_parameter=share_parameter,
                                   allow_ip=allow_ip,share_permission=share_permission,share_host=share_host)
                    data_insert.save()
        #修改完成后拷贝
        if not share_host:
            commands.getoutput('cp %s %s'%(NFS_TMP_FILE,NFS_SHARE_FILE))
            commands.getoutput('rm -f %s'%(NFS_TMP_FILE))
            commands.getoutput('exportfs -rv')
        else:
            commands.getoutput('scp %s %s:%s'%(NFS_TMP_FILE,share_host,NFS_SHARE_FILE))
            commands.getoutput('rm -f %s'%(NFS_TMP_FILE))
            exec_commands(connect(share_host,user_name),'exportfs -rv')
        return HttpResponse('ok')
    if not user_dict:
        return redirect('/login')
    return HttpResponse('no data')

def del_share_storage(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if req.method == 'POST':
        user_name = user_dict['user_name']
        if user_name != 'root':
            return HttpResponse('failed')
        folder_id = req.POST.get('folder_id',None)
        if folder_id:
            try:
                row_data = Storage.objects.get(id=folder_id)
                folder_name = row_data.folder_name
                share_host    = row_data.share_host
            except:
                return HttpResponse('failed')
        #复制nfs配置文件到本地tmp
        commands.getoutput('rm -f %s'%(NFS_TMP_FILE))
        commands.getoutput('scp %s:%s %s'%(share_host,NFS_SHARE_FILE,NFS_TMP_FILE))
        with open(NFS_TMP_FILE,'r') as r:
            file_lines=r.readlines()
        with open(NFS_TMP_FILE,'w') as w:     
            for l in file_lines:
                #如果存在就修改
                if l.strip() and l.strip().split()[0] == folder_name:
                    index_num = file_lines.index(l)
                    del file_lines[index_num:index_num]
                else:
                    w.write(l) 
            #判断在数据库中是否存在，如果存在，删除该行
            row_data = Storage.objects.filter(folder_name=folder_name)
            if row_data:
                row_data.delete()
            #修改完成后拷贝
            commands.getoutput('scp %s %s:%s'%(NFS_TMP_FILE,share_host,NFS_SHARE_FILE))
            commands.getoutput('rm -f %s'%(NFS_TMP_FILE))
            exec_commands(connect(share_host,user_name),'exportfs -rv')
        return HttpResponse('ok')
    if not user_dict:
        return redirect('/login')
    return HttpResponse('no data')