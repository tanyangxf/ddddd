#coding:utf-8
from django.shortcuts import render_to_response,HttpResponse
from monitor.models import Host
from clusmgr_api.tree_api import get_dir_content
import json,os
from remote_help import exec_commands,connect
import commands
from numpy.distutils.conv_template import process_str
# Create your views here.
#job文件管理，file_tree.html调用文件api
def file_tree(req):
    return render_to_response('clusmgr/file_tree.html')
def dir_tree(req):
    return render_to_response('clusmgr/dir_tree.html')


def mgr_dir_tree(req):
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
    data = exec_commands(connect(host_name,'root'),'ls -Fa %s | grep "/$"' % folder)
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
    
#文件管理器主页布局
def mgr_file(req):
    node_data = Host.objects.values('host_name').order_by('id')
    return render_to_response('clusmgr/mgr_file.html',{'node_data':node_data})

#文件管理器显示内容
def dir_content(req):
    if req.method == 'POST':
        folder_id = req.POST['folder_id']
        if folder_id:
            host_name = folder_id.split(':')[0]
            folder = folder_id.split(':')[1]
            #ls -l --time-style '+%Y/%m/%d %H:%M:%S'
        data = exec_commands(connect(host_name,'root'),'ls -la --time-style %s %s' % ("'+%Y-%m-%d %H:%M:%S'",folder))
        if data == 'failed':
            data = u'主机连接失败！'
            data = json.dumps(data)
            return HttpResponse(data)
        #data为元组，('获取的目录','错误信息')
        if data[0]:
            folder_detail_data = []
            #['-rw-r--r--   1 tanyang staff 8196 2016/09/21 00:29:59 .DS_Store', 'drwxr-xr-x  14 tanyang staff  476 2016/10/19 12:52:17 .git']
            #排除./和../和total
            folder_list = data[0].split('\n')[1:]
            for folder_detail in folder_list:
                if folder_detail:
                    folder_temp_data = {}
                    folder_detail = folder_detail.split()
                    folder_temp_data['permission'] = folder_detail[0]
                    if folder_detail[0][0] == 'd':
                        folder_temp_data['file_type'] = u'文件夹'
                    else:
                        folder_temp_data['file_type'] = u'文件'
                    folder_temp_data['username'] = folder_detail[2]
                    folder_temp_data['group'] = folder_detail[3]
                    folder_temp_data['modify_time'] = folder_detail[5] + ' ' + folder_detail[6]
                    folder_temp_data['size'] = folder_detail[4]
                    folder_temp_data['name'] = folder_detail[-1]
                    folder_detail_data.append(folder_temp_data)
        data = json.dumps(folder_detail_data)
        return HttpResponse(data)
    return render_to_response('clusmgr/dir_content.html')
    
#获取进程信息，节点树
def mgr_process(req):
    node_data = Host.objects.only('host_name').order_by('id')
    if req.method == 'POST':
        host_name = req.POST['host_name']
        process_data = exec_commands(connect(host_name,'root'),'ps aux')
        if process_data == 'failed':
            process_data = u'主机连接失败！'
            process_data = json.dumps(process_data)
            return HttpResponse(process_data)
        #除去首行信息
        if process_data[0]:
            process_detail_data = []
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
                    process_detail_data.append(process_temp_data)
        process_detail_data = json.dumps(process_detail_data)
        return HttpResponse(process_detail_data)
    return render_to_response('clusmgr/mgr_process.html',{'node_data':node_data})

def vnc_login(req):
    pass


