#coding:utf-8
import json
from django.shortcuts import HttpResponse,redirect
from monitor.models import Host
def get_node_tree(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('login')
    node = u"节点列表"
    nodetree = {'id':'all_node'}
    nodetree['children'] = []
    nodetree['text'] = node
    nodetree['icon'] = "glyphicon glyphicon-folder-close"
    #提前定义数据格式
    data = {}
    node_data = Host.objects.only('host_name').order_by('id')
    for i in node_data:
        node_name = i.host_name
        data = {"id":node_name,"text":node_name,"children":False,"icon":"glyphicon glyphicon-file"}
        nodetree['children'].append(data)
    nodetree = json.dumps(nodetree)
    return HttpResponse(nodetree)
