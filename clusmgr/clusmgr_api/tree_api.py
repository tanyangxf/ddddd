#coding:utf-8
import os
import json
from django.shortcuts import HttpResponse,redirect
from clusmgr.remote_help import curr_user_cmd
import commands
#通过http://url/?id=xxx访问
def get_dir_tree(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        data = 'no data'
        return HttpResponse(data)
    user_name = user_dict['user_name']
    #结尾不能有/
    folder = '/'
    #点击事件获取到id，jstree是通过?id=xxx获取id的值来生成树结构
    head = req.GET['id']
    if head != '#':
        folder = head
    if ":" in folder:
        folder = folder.split(':')[1]
    #id采用主机名+文件夹的方式
    dirtree = {"id":folder}
    dirtree['children'] = []
    #"text"为文件夹的名字， jstree通过id来生成
    if folder == '/':
        dirtree['text'] = ' ' + folder
    else:
        dirtree['text'] = os.path.basename(folder)
    #data : (0,xxx),(1,err)
    data = commands.getstatusoutput(curr_user_cmd(user_name,'ls -Fa %s | grep "/$"' % folder))
    if not data[0]:
        for item in data[1].split('\n'):
            if item and item != './' and item != "../":
                #结尾有”/"去掉
                item = item[:-1]
                folder_id = os.path.join(folder,item)
                data = {"id":folder_id,"text":item,"children":True,"icon":'glyphicon glyphicon-folder-close'}
                dirtree['children'].append(data)
    dirtree['icon'] = 'glyphicon glyphicon-folder-close'
    dirtree = json.dumps(dirtree)
    return HttpResponse(dirtree)

def get_file_tree(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        data  = 'no data'
        return HttpResponse(data)
    user_name = user_dict['user_name']
    folder = '/'
    
    #点击事件获取到id
    head = req.GET['id']
    if head != '#':
        folder = head
    #主目录插入
    dirtree={'id':folder}
    dirtree['children'] = []
    #提前定义数据格式
    data = {}
    data["id"] = ''
    if folder == '/':
        dirtree['text'] = ' ' + folder
    else:
        dirtree['text'] = os.path.basename(folder)
    data = commands.getstatusoutput(curr_user_cmd(user_name,'ls -Fa %s' % folder))
    #0代正确执行
    if not data[0]:
        for item in data[1].split('\n'):
            if item and item != './' and item != "../" and item[-1] != '@':
                #结尾有”/"去掉
                if item[-1] == '/':
                    item = item[:-1]
                    folder_id = os.path.join(folder,item)
                    data = {"id":folder_id,"text":item,"children":True,"icon":'glyphicon glyphicon-folder-close'}
                    dirtree['children'].append(data)
                elif item[-1] == '*':
                    item = item[:-1]
                    folder_id = os.path.join(folder,item)
                    data = {"id":folder_id,"text":item,"icon":'glyphicon glyphicon-file'}
                    dirtree['children'].append(data) 
                else:
                    folder_id = os.path.join(folder,item)
                    data = {"id":folder_id,"text":item,"icon":'glyphicon glyphicon-file'}
                    dirtree['children'].append(data) 
    dirtree['icon'] = 'glyphicon glyphicon-folder-close'
    dirtree = json.dumps(dirtree)
    return HttpResponse(dirtree)



'''
def get_dir_tree(req):
    #结尾不能有/
    folder = '/'
    
    #点击事件获取到id   #/node1
    head = req.GET['id']
    if head != '#':
        folder = head
    #判断结尾是否有/符号，去掉
    
    #主目录插入
    dirtree={'id':folder}
    dirtree['children'] = []
    dirtree['icon'] = 'glyphicon glyphicon-folder-close'  
    #提前定义数据格式
    data = {}
    data["id"] = ''
    if os.path.isdir(folder):
        if folder == '/':
            dirtree['text'] = ' ' + folder
        else:
            dirtree['text'] = os.path.basename(folder)
        for item in os.listdir(folder):
            if item:
                if os.path.isdir(os.path.join(folder,item)):
                    data = {"id":os.path.join(folder,item),"text":item,"children":True,"icon":'glyphicon glyphicon-folder-close'}
                    dirtree['children'].append(data)
                    
                    
                #注释开始：    
                if os.path.isdir(os.path.join(folder,item)):
                    #判断是否有子目录
                    sub_folder = os.path.join(folder,item)
                    for sub_item in os.listdir(sub_folder):
                        if os.path.isdir(os.path.join(sub_folder,sub_item)):
                            data = {"id":sub_folder,"text":item,"children":True,"icon":'glyphicon glyphicon-folder-close'}
                            dirtree['children'].append(data)
                            break
                    #判断之前是否存在,并且自己本身是目录，但是没有子目录
                    if data["id"] != sub_folder:
                        data = {"id":sub_folder,"text":item,"icon":'glyphicon glyphicon-folder-close'}
                        dirtree['children'].append(data)
                #注释结束

        #dirtree = {"id":"test1","text":"Root node","children":[{"id":"test2","text":"Child node 1","children":True},{"id":"test3","text":"Child node 2"}]}
        dirtree = json.dumps(dirtree)
        return HttpResponse(dirtree)
    else:
        dirtree = json.dumps(dirtree)
        return HttpResponse(dirtree)
'''
#通过http://url/?id=xxx访问

'''
def get_file_tree(req):
    #结尾不能有/
    folder = '/'
    
    #点击事件获取到id
    head = req.GET['id']
    if head != '#':
        folder = head
        
    #判断结尾是否有/符号，去掉
    
    #主目录插入
    dirtree={'id':folder}
    dirtree['children'] = []
    #提前定义数据格式
    data = {}
    data["id"] = ''
    if os.path.isdir(folder):
        if folder == '/':
            dirtree['text'] = ' ' + folder
        else:
            dirtree['text'] = os.path.basename(folder)
        for item in os.listdir(folder):
            if item:
                sub_folder = os.path.join(folder,item)
                if os.path.isdir(sub_folder):
                    data = {"id":sub_folder,"text":item,"children":True,"icon":'glyphicon glyphicon-folder-close'}
                    dirtree['children'].append(data)
                    
                    
                    #注释开始：
                    #判断目录下面是否有文件或者目录
                    for sub_item in os.listdir(sub_folder):
                        if sub_item is not None:
                            data = {"id":sub_folder,"text":item,"children":True,"icon":'glyphicon glyphicon-folder-close'}
                            dirtree['children'].append(data)
                            break
                    if data["id"] != sub_folder:
                        data = {"id":sub_folder,"text":item,"icon":'glyphicon glyphicon-folder-close'}
                        dirtree['children'].append(data)
                        #注释结束
                else:
                    data = {"id":sub_folder,"text":item,"icon":'glyphicon glyphicon-file'}
                    dirtree['children'].append(data) 
                
        dirtree['icon'] = 'glyphicon glyphicon-folder-close'           
        dirtree = json.dumps(dirtree)
        return HttpResponse(dirtree)
    else:
        dirtree['icon'] = 'glyphicon glyphicon-file'
        dirtree = json.dumps(dirtree)
        return HttpResponse(dirtree)
'''     

