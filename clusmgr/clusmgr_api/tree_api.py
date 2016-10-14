#coding:utf-8
import os
import json
from django.shortcuts import HttpResponse


#通过http://url/?id=xxx访问
def get_dir_tree(req):
    #结尾不能有/
    folder = '/Users/tanyang/yicloud/'
    
    #点击事件获取到id
    head = req.GET['id']
    if head != '#':
        folder = head
        
    #判断结尾是否有/符号，去掉
    if folder[-1] == '/':
        folder = folder[:-1]
    #主目录插入
    dirtree={'id':folder}
    dirtree['children'] = []
    dirtree['icon'] = 'glyphicon glyphicon-folder-close'    
    #提前定义数据格式
    data = {}
    data["id"] = ''
    if os.path.isdir(folder):
        dirtree['text']=os.path.basename(folder)
        for item in os.listdir(folder):
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
        #dirtree = {"id":"test1","text":"Root node","children":[{"id":"test2","text":"Child node 1","children":True},{"id":"test3","text":"Child node 2"}]}
        dirtree = json.dumps(dirtree)
        return HttpResponse(dirtree)
    else:
        dirtree = json.dumps(dirtree)
        return HttpResponse(dirtree)

#通过http://url/?id=xxx访问

def get_file_tree(req):
    #结尾不能有/
    folder = '/Users/tanyang/yicloud/'
    
    #点击事件获取到id
    head = req.GET['id']
    if head != '#':
        folder = head
        
    #判断结尾是否有/符号，去掉
    if folder[-1] == '/':
        folder = folder[:-1]
    #主目录插入
    dirtree={'id':folder}
    dirtree['children'] = []
    #提前定义数据格式
    data = {}
    data["id"] = ''
    if os.path.isdir(folder):
        dirtree['text']=os.path.basename(folder)
        for item in os.listdir(folder):
            sub_folder = os.path.join(folder,item)
            if os.path.isdir(sub_folder):
                #判断目录下面是否有文件或者目录
                for sub_item in os.listdir(sub_folder):
                    if sub_item is not None:
                        data = {"id":sub_folder,"text":item,"children":True,"icon":'glyphicon glyphicon-folder-close'}
                        dirtree['children'].append(data)
                        break
                if data["id"] != sub_folder:
                    data = {"id":sub_folder,"text":item,"icon":'glyphicon glyphicon-folder-close'}
                    dirtree['children'].append(data)
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