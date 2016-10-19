#coding:utf-8
from django.shortcuts import render_to_response
from monitor.models import Host

# Create your views here.
#job文件管理，file_tree.html调用文件api
def file_tree(req):
    return render_to_response('clusmgr/file_tree.html')
def dir_tree(req):
    return render_to_response('clusmgr/dir_tree.html')

#文件管理器主页布局
def mgr_file(req):
    node_data = Host.objects.values('host_name').order_by('id')
    return render_to_response('clusmgr/mgr_file.html',{'node_data':node_data})

#文件管理器显示内容
def mgr_file_content(req):
    if req.method == 'POST':
        data = req.POST['data_select']
        print data
    return render_to_response('clusmgr/mgr_file_content.html')
    

