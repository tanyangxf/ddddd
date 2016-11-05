#coding:utf-8
import json
from django.shortcuts import HttpResponse,redirect, render
from sysmgr.models import User
def get_user_tree(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('login')
    node = u"用户列表"
    nodetree = {'id':'all_user'}
    nodetree['children'] = []
    nodetree['text'] = node 
    nodetree['icon'] = "glyphicon glyphicon-folder-close"
    #提前定义数据格式
    data = {}
    node_data = User.objects.only('user_name').order_by('id')
    for i in node_data:
        user_name = i.user_name
        data = {'id':user_name,'text':user_name,"children":False,"icon":"glyphicon glyphicon-file"}
        nodetree['children'].append(data)
    nodetree = json.dumps(nodetree)
    return HttpResponse(nodetree)
