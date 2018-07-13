#coding:utf-8
from django.shortcuts import HttpResponse, redirect,render
from monitor.models import Host
from sysmgr.models import User
import json,os
from remote_help import exec_commands,connect,curr_user_cmd,upload_module,download_module
from django.conf import settings
import hashlib
import commands
import socket
from config.config import *
from django.views.decorators.csrf import csrf_exempt
import pwd
import re
from wsgiref.util import FileWrapper
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# Create your views here.
#job文件管理，file_tree.html调用文件api
def file_tree(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    return render(req,'clusmgr/file_tree.html')
def dir_tree(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    return render(req,'clusmgr/dir_tree.html')

def mgr_dir_tree(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        data  = 'no data'
        return HttpResponse(data)
    user_name = user_dict['user_name']
    #结尾不能有/
    folder = '/'
    host_name = req.GET['host_name']
    #点击事件获取到id，jstree是通过?id=xxx获取id的值来生成树结构
    head = req.GET['id']
    if head != '#':
        folder = head
    if ":" in folder:
        folder = folder.split(':')[1]
    #id采用主机名+文件夹的方式
    dirtree = {"id":host_name + ":" + folder}
    dirtree['children'] = []    
    #"text"为文件夹的名字， jstree通过id来生成
    if folder == '/':
        dirtree['text'] = folder
    else:
        dirtree['text'] = os.path.basename(folder)
    #判断目录名是否有空格
    folder_temp = ''
    for s in os.path.basename(folder):
        if s.isspace():
            s = s.replace(s,'\\' + s)
        folder_temp = folder_temp + s
    folder = os.path.dirname(folder) + '/' + folder_temp 
    data = exec_commands(connect(host_name,'root'),curr_user_cmd(user_name,'ls -Fa %s | grep "/$"' % folder))
    if data == 'failed':
        dirtree['text'] = u'主机连接失败！'
        dirtree = json.dumps(dirtree)
        return HttpResponse(dirtree)
    for item in data[0].split('\n'):
        if item and item != './' and item != "../":
            #结尾有”/"去掉
            item = item[:-1]
            folder_id = os.path.join(folder,item)
            data = {"id":host_name + ":" + folder_id,"text":item,"children":True,"icon":'glyphicon glyphicon-folder-close'}
            dirtree['children'].append(data)
    dirtree['icon'] = 'glyphicon glyphicon-folder-close'
    dirtree = json.dumps(dirtree)
    return HttpResponse(dirtree)
    

def mgr_file_index(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    return render(req,'clusmgr/mgr_file.html')

def get_dir_content(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    if req.method == 'POST': 
        try:    
            user_name = user_dict['user_name']  
            folder = req.POST.get('folder_id')
            #判断目录名是否有空格
            if os.path.basename(folder).count(' '):
                folder_temp = os.path.basename(folder).replace(' ','\\' + ' ')
                folder = os.path.dirname(folder) + '/' + folder_temp 
            data = commands.getstatusoutput(curr_user_cmd(user_name,'ls -la --time-style %s %s' % ("'+%Y-%m-%d %H:%M:%S'",folder)))
            if data[0]:
                data = u'failed'
                data = json.dumps(data)
                return HttpResponse(data)
            #data为元组，('获取的目录','错误信息')
            folder_data_info = {}
            folder_detail_list = []
            file_count = 0
                #['-rw-r--r--   1 tanyang staff 8196 2016/09/21 00:29:59 .DS_Store', 'drwxr-xr-x  14 tanyang staff  476 2016/10/19 12:52:17 .git']
                #排除./和../和total
            folder_list = data[1].split('\n')[1:]
            for folder_detail in folder_list:
                if folder_detail and folder_detail[0][0] != 'l':
                    folder_temp_data = {}
                    #判断文件名中空格问题
                    folder_temp_detail = folder_detail
                    folder_detail = folder_detail.split()
                    if folder_detail[7] != '.' and folder_detail[7] != '..':
                        folder_temp_data['permission'] = folder_detail[0]
                        if folder_detail[0][0] == 'd':
                            folder_temp_data['file_type'] = u'文件夹'
                        else:
                            folder_temp_data['file_type'] = u'文件'
                        folder_temp_data['username'] = folder_detail[2]
                        folder_temp_data['group'] = folder_detail[3]
                        folder_temp_data['modify_time'] = folder_detail[5] + ' ' + folder_detail[6]
                        folder_temp_data['size'] = folder_detail[4]
                        #判断文件名中空格问题
                        folder_temp_data['name'] = folder_temp_detail.split(folder_detail[6] + ' ',2)[-1]
                        folder_detail_list.append(folder_temp_data)
                        file_count = file_count + 1
            if not folder_detail_list:
                folder_temp_data = {}
                folder_temp_data['name'] = u'没有任何文件或者文件夹!'
                folder_detail_list.append(folder_temp_data)
            folder_data_info['total'] = file_count
            folder_data_info['rows'] = folder_detail_list
            folder_data_info = json.dumps(folder_data_info)
            return HttpResponse(folder_data_info)
        except Exception,e:
            return HttpResponse(e)
    else:
        if not user_dict:
            return redirect("/login")
        return render(req,'clusmgr/dir_content.html')
    
@csrf_exempt
def file_upload(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    #upload_module(connect('172.16.123.1','tanyang'),'views.py','/Users/tanyang/4.sh')  
    folder_name = req.POST.get('folder_name',None)
    file_data =  req.FILES['input-folder-2']
    file_name =  req.FILES['input-folder-2'].name
    user_name = user_dict['user_name']
    if user_name != 'root':
        tempfile = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(64)))
        touch_cmd = 'su - %s -c "touch %s"'%(user_name,os.path.join(folder_name,tempfile))
        folder_iswrite = commands.getstatusoutput(touch_cmd)
        if folder_iswrite[0] != 0:
            process_detail_data = json.dumps('上传失败，目录不可写')
            return HttpResponse(process_detail_data)
        commands.getstatusoutput('rm -f %s'%os.path.join(folder_name,tempfile))
    with open(os.path.join(folder_name,file_name), 'wb+') as f:
        for chunk in file_data.chunks():
            f.write(chunk)
    if user_name != 'root':
        os.chown(os.path.join(folder_name,file_name), pwd.getpwnam(user_name).pw_uid, pwd.getpwnam(user_name).pw_gid)
    process_detail_data = json.dumps('上传成功')
    return HttpResponse(process_detail_data)

def file_upload_index(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    return render(req,'clusmgr/file_upload_index.html')

@csrf_exempt
def file_download(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    try:
        #user_name = user_dict['user_name']
        file_name = req.GET.get('file_name',None)
        folder_name = req.GET.get('folder_name',None)
        if folder_name == '/':
            file_path = folder_name + file_name
        else:
            file_path = folder_name + '/' + file_name
        wrapper = FileWrapper(file(file_path))
        response = HttpResponse(wrapper, content_type='text/plain')
        response['Content-Length'] = os.path.getsize(file_path)
        response['Content-Encoding'] = 'utf-8'
        file_name = file_name.encode('utf-8')
        file_name = re.sub(r'\s+','%20',file_name)
        response['Content-Disposition'] = 'attachment;filename=%s' % file_name
        return response
    except Exception:
        return HttpResponse(u'非法操作')

def file_delete(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    if req.method == 'POST':
        user_name = user_dict['user_name']
        file_name = req.POST.get('file_name',None)
        folder_name = req.POST.get('folder_name',None)
        file_name = re.sub(r'\s+','\ ',file_name)
        #folder_name = re.sub(r'\s+','\ ',folder_name)
        if folder_name == '/':
            file_path = folder_name + file_name
        else:
            file_path = folder_name + '/' + file_name
        cmd = curr_user_cmd(user_name,'rm -rf %s')%(file_path)
        del_result = commands.getstatusoutput(cmd)
        if del_result[0]:
            return HttpResponse('failed')
        else:
            return HttpResponse('ok')
    else:
        return HttpResponse(u'非法操作')
#获取进程信息，节点树
def mgr_process(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    node_data = Host.objects.only('host_name').order_by('id')
    if req.method == 'POST':
        if not user_dict:
            data  = "no data"
            return HttpResponse(data)
        try:
            user_name = user_dict['user_name']
            host_name = req.POST['host_name']
            process_data = exec_commands(connect(host_name,'root'),curr_user_cmd(user_name,'ps aux'))
            if process_data[1] == 'failed':
                process_data = u'主机连接失败！'
                process_data = json.dumps(process_data)
                return HttpResponse(process_data)
            process_detail_data = {}
            #除去首行信息
            process_detail_list = []
            if process_data[0]:
                process_data = process_data[0].split('\n')[1:] 
                for process_detail in process_data:
                    if process_detail:
                        process_temp_data = {} 
                        process_detail = process_detail.split()
                        process_temp_data['user'] = process_detail[0]
                        process_temp_data['pid'] = process_detail[1]
                        process_temp_data['cpu'] = process_detail[2]
                        process_temp_data['mem'] = process_detail[3]
                        process_temp_data['vsz'] = process_detail[4]
                        process_temp_data['rss'] = process_detail[5]
                        process_temp_data['stat'] = process_detail[7]
                        process_temp_data['started'] = process_detail[8]
                        process_temp_data['time'] = process_detail[9]
                        process_name = ''
                        for cmd in process_detail[10:]:
                            process_name = process_name + cmd + ' '
                        process_temp_data['name'] = process_name
                        process_detail_list.append(process_temp_data)
            process_detail_data['rows'] = process_detail_list
            process_detail_data = json.dumps(process_detail_data)
            return HttpResponse(process_detail_data)
        except Exception:
            return HttpResponse('falied')
    if not user_dict:
        return redirect("/login")
    return render(req,'clusmgr/mgr_process.html',{'node_data':node_data})

def process_stop(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    user_name = user_dict['user_name']
    if req.method == 'POST':
        try:
            pids = req.POST.get('pid',None)
            host_name = req.POST.get('host_name',None)
            for p in pids.split(','):
                exec_commands(connect(host_name,'root'),curr_user_cmd(user_name,'kill -9 %s' % p))
            return HttpResponse('ok')
        except Exception:
            return HttpResponse('failed')
    else:
        return HttpResponse('非法操作')

def vnc_login(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    user_name = user_dict['user_name']
    if user_name == 'root':
        user_home = User.objects.filter(user_name='superuser').values('user_home')[0]['user_home']
    else:
        user_home = User.objects.filter(user_name=user_name).values('user_home')[0]['user_home']
    view_only = req.GET.get('view_only', 'false') # False can control the or true can only view

    # The proxy server IP and port, this usually use school server LAN IP (127.0.0.1, 6080 is the default port)
    host = req.get_host().split(':')[0]
    port = settings.VNC_PROXY_PORT
    password = hashlib.sha512(user_name).hexdigest() 
    #创建vnc目录，设置密码
    commands.getoutput(curr_user_cmd(user_name,'mkdir %s/.vnc'%user_home))
    commands.getoutput(curr_user_cmd(user_name,'echo %s|vncpasswd -f>%s/.vnc/passwd'%(password, user_home)))
    commands.getoutput(curr_user_cmd(user_name,'chmod 600 %s/.vnc/passwd'%(user_home)))
    process_id = commands.getoutput(curr_user_cmd(user_name,"ps -U %s|grep Xvnc|awk '{print \$1}'"%user_name))
    #判断vnc进程是否存在
    if process_id:
        for process in process_id.split('\n'):
            vnc_id = commands.getoutput(curr_user_cmd(user_name,"vncserver -list|grep %s|awk '{print \$1}'"%process))
            vnc_id = int(vnc_id.split(':')[-1]) + 5900
            #修改配置文件
            vncfg_is_exsits = False
            with open(VNC_TOKEN,'r') as r:
                file_lines=r.readlines()
            with open(VNC_TOKEN,'w') as w:
                for l in file_lines:
                    if l.strip().startswith('%s:'%user_name):
                        vncfg_is_exsits = True
                        index_num = file_lines.index(l)
                        file_lines[index_num] = '%s:'%user_name + '  ' + '127.0.0.1:%s'%vnc_id  + '\n'
                        w.write(file_lines[index_num])
                    else:
                        w.write(l)  
                if not vncfg_is_exsits:
                    add_lines = '%s:'%user_name + '  ' + '127.0.0.1:%s'%vnc_id  + '\n'
                    w.write(add_lines) 
            #只保存一条记录。
            break
    else:
        #进程不存在，写token文件，启动vncserver，然后获取进程id
        commands.getoutput(curr_user_cmd(user_name,'vncserver'))
        process_id = commands.getoutput(curr_user_cmd(user_name,"ps -U %s|grep Xvnc|awk '{print \$1}'"%user_name))
        vnc_id = commands.getoutput(curr_user_cmd(user_name,"vncserver -list|grep %s|awk '{print \$1}'"%process_id))
        vnc_id = int(vnc_id.split(':')[-1]) + 5900
        vncfg_is_exsits = False
        with open(VNC_TOKEN,'r') as r:
            file_lines=r.readlines()
        with open(VNC_TOKEN,'w') as w:
            for l in file_lines:
                if l.strip().startswith('%s:'%user_name):
                    vncfg_is_exsits = True
                    index_num = file_lines.index(l)
                    file_lines[index_num] = '%s:'%user_name + '  ' + '127.0.0.1:%s'%vnc_id  + '\n'
                    w.write(file_lines[index_num])
                else:
                    w.write(l)  
            if not vncfg_is_exsits:
                add_lines = '%s:'%user_name + '  ' + '127.0.0.1:%s'%vnc_id  + '\n'
                w.write(add_lines)  
    host_token = user_name
    return render(req, 'clusmgr/vnc_auto.html',{'host':host,'port':port,'password':password,'token':host_token,'view_only':view_only})

def vnc_mgr(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    return render(req, 'clusmgr/vnc_mgr.html')

def get_vnc_list(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    if req.method == 'POST': 
        user_name = user_dict['user_name']
        process_id = commands.getoutput(curr_user_cmd(user_name,"ps -U %s|grep Xvnc|awk '{print \$1}'"%user_name))
        vnc_temp_list = []
        vnc_temp_dict = []
        vnc_list_info = {}
        #判断vnc进程是否存在
        if process_id:
            
            host_name = req.get_host().split(':')[0]
            vnc_id = commands.getoutput(curr_user_cmd(user_name,"vncserver -list|grep %s|awk '{print \$1}'"%process_id))
            vnc_id = int(vnc_id.split(':')[-1]) + 5900
            vnc_temp_dict['host_name'] = host_name
            vnc_temp_dict['vnc_id'] = vnc_id
            vnc_temp_dict['process_id'] = process_id
            vnc_temp_dict['user_name'] = user_name
            vnc_temp_dict['status'] = u'正常'
            
            vnc_temp_list.append(vnc_temp_dict)
            vnc_list_info['rows'] = vnc_temp_list
            vnc_list_info = json.dumps(vnc_list_info)
            return HttpResponse(vnc_list_info)
        else:
            vnc_temp_dict['host_name'] = u'无记录'
            vnc_temp_list.append(vnc_temp_dict)
            vnc_list_info['rows'] = vnc_temp_list
            vnc_list_info = json.dumps(vnc_list_info)
            return HttpResponse(vnc_list_info)
    else:
        return HttpResponse(u'非法操作')
    
def vnc_create(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    if req.method == 'POST': 
        user_name = user_dict['user_name']
        if user_name == 'root':
            user_home = User.objects.filter(user_name='superuser').values('user_home')[0]['user_home']
        else:
            user_home = User.objects.filter(user_name=user_name).values('user_home')[0]['user_home']
        # The proxy server IP and port, this usually use school server LAN IP (127.0.0.1, 6080 is the default port)
        process_id = commands.getoutput(curr_user_cmd(user_name,"ps -U %s|grep Xvnc|awk '{print \$1}'"%user_name))
        #判断vnc进程是否存在
        if process_id:
            return HttpResponse('ok')
        else:
            password = hashlib.sha512(user_name).hexdigest() 
            #创建vnc目录，设置密码
            commands.getoutput(curr_user_cmd(user_name,'mkdir %s/.vnc'%user_home))
            commands.getoutput(curr_user_cmd(user_name,'echo %s|vncpasswd -f>%s/.vnc/passwd'%(password, user_home)))
            commands.getoutput(curr_user_cmd(user_name,'chmod 600 %s/.vnc/passwd'%(user_home)))
            #进程不存在，写token文件，启动vncserver，然后获取进程id
            commands.getoutput(curr_user_cmd(user_name,'vncserver'))
            process_id = commands.getoutput(curr_user_cmd(user_name,"ps -U %s|grep Xvnc|awk '{print \$1}'"%user_name))
            vnc_id = commands.getoutput(curr_user_cmd(user_name,"vncserver -list|grep %s|awk '{print \$1}'"%process_id))
            vnc_id = int(vnc_id.split(':')[-1]) + 5900
            vncfg_is_exsits = False
            with open(VNC_TOKEN,'r') as r:
                file_lines=r.readlines()
            with open(VNC_TOKEN,'w') as w:
                for l in file_lines:
                    if l.strip().startswith('%s:'%user_name):
                        vncfg_is_exsits = True
                        index_num = file_lines.index(l)
                        file_lines[index_num] = '%s:'%user_name + '  ' + '127.0.0.1:%s'%vnc_id  + '\n'
                        w.write(file_lines[index_num])
                    else:
                        w.write(l)  
                if not vncfg_is_exsits:
                    add_lines = '%s:'%user_name + '  ' + '127.0.0.1:%s'%vnc_id  + '\n'
                    w.write(add_lines)  
            return HttpResponse('ok')
    else:
        return HttpResponse(u'非法操作')

def vcn_del(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    if req.method == 'POST': 
        user_name = user_dict['user_name']
        process_id = req.POST.get('process_id',None)
        #判断vnc进程是否存在
        if process_id:
            cmd_result = commands.getstatusoutput(curr_user_cmd(user_name,'kill -9  %s'%process_id))
            if not cmd_result[0]:
                return HttpResponse('ok')
            else:
                return HttpResponse('failed')
        else:
            return HttpResponse('failed')
    else:
        return HttpResponse(u'非法操作')
    