#coding:utf-8
from django.shortcuts import render_to_response

# Create your views here.
def file_tree(req):
    return render_to_response('clusmgr/file_tree.html')
def dir_tree(req):
    return render_to_response('clusmgr/dir_tree.html')

