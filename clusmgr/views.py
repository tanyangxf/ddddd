#coding:utf-8
from django.shortcuts import render_to_response, HttpResponse
import os
import json
# Create your views here.
def dir_tree(req):
    return render_to_response('clusmgr/dir_tree.html')
def get_dir_tree(req):
    folder = '/Users/tanyang/yicloud'
    head = req.GET['id']
    if head != '#':
        folder = os.path.join(folder,head) 
    dirtree={'id':os.path.basename(folder)}
    dirtree['children'] = []
    data = {}
    data["id"] = ''
    
    print head
    if os.path.isdir(folder):
        dirtree['text']=os.path.basename(folder)
        for item in os.listdir(folder):
            if os.path.isdir(os.path.join(folder,item)):
                #判断是否有子目录
                sub_folder = os.path.join(folder,item)
                for sub_item in os.listdir(sub_folder):
                    if os.path.isdir(os.path.join(sub_folder,sub_item)):
                        data = {"id":item,"text":item,"children":True}
                        dirtree['children'].append(data)
                        break
                #判断之前是否存在
                if data["id"] != item:
                    data = {"id":item,"text":item}
                    dirtree['children'].append(data)
        #dirtree = {"id":"test1","text":"Root node","children":[{"id":"test2","text":"Child node 1","children":True},{"id":"test3","text":"Child node 2"}]}
        print dirtree
        dirtree = json.dumps(dirtree)
        return HttpResponse(dirtree)
    dirtree = json.dumps(dirtree)
    return HttpResponse(dirtree)

                     
'''
{"text": "clusmgr", "children": [{"text": "__init__.py"}]     }

{"id":1,"text":"Root node","children":[
    {"id":2,"text":"Child node 1","children":true},
    {"id":3,"text":"Child node 2"}
  ]
}   
'''  
'''
def get_dir_tree(req):

    folder = '/Users/tanyang/yicloud'
    if req.method == 'POST':
        dirtree={'children':[]}
        folder = os.path.join(folder,req.POST['folder_name'])
        if os.path.isdir(folder):
            dirtree['text']=os.path.basename(folder)
            for item in os.listdir(folder):
                if os.path.isdir(os.path.join(folder,item)):
                    dirtree['children'].append(item)
            dirtree = json.dumps(dirtree)
            print dirtree
            return HttpResponse(dirtree)
    else:
        dirtree={'children':[]}
        if os.path.isdir(folder):
            dirtree['text']=os.path.basename(folder)
            for item in os.listdir(folder):
                if os.path.isdir(os.path.join(folder,item)):
                    dirtree['children'].append(item)
            dirtree = json.dumps(dirtree)
            return HttpResponse(dirtree)
'''
class GetFileWithTree():
    def getFileTree(self,folder):
        '''
            :param folder:文件目录
            :return:目录的字典
        '''
        dirtree={'children':[]}
        if os.path.isfile(folder):
            return {'text':os.path.basename(folder),'icon':'glyphicon glyphicon-leaf'}
        else:
            basename=os.path.basename(folder)
            dirtree['text']=basename
            for item in os.listdir(folder):
                #递归获取所有目录和文件
                dirtree['children'].append(self.getFileTree(os.path.join(folder,item)))
                #dirtree['children'].append(item)
            return dirtree

    def getFileTreeWithJson(self,folder):
        '''
            将文件夹生成树状的json串
            :param folder: 文件夹
            :return:文件树json
        '''
        return json.dumps(self.getFileTree(folder))
class GetDirWithTree():
    def getDirTree(self,folder):
        '''
            :param folder:文件目录
            :return:目录的字典
        '''
        dirtree={'children':[]}
        if os.path.isdir(folder):
            dirtree['text']=folder
            for item in os.listdir(folder):
                if os.path.isdir(os.path.join(folder,item)):
                    #判断是否有子目录
                    sub_folder = os.path.join(folder,item)
                    for sub_item in os.listdir(sub_folder):
                        if os.path.isdir(os.path.join(sub_folder,sub_item)):
                            data = {"id":item,"text":item,"children":'true'}
                            dirtree['children'].append(data)
                            break
                    #判断之前是否存在
                    if data["id"] != item:
                        data = {"id":item,"text":item}
                        dirtree['children'].append(data)                            
            return dirtree

 

    def getDirTreeWithJson(self,folder):
        '''
            将文件夹生成树状的json串
            :param folder: 文件夹
            :return:文件树json
        '''
        return json.dumps(self.getDirTree(folder))    
test = GetDirWithTree()
print test.getDirTreeWithJson('/Users/tanyang/yicloud/')