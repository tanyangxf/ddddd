from django.shortcuts import render_to_response,HttpResponse
from monitor.models import Host
from django.shortcuts import redirect

# Create your views here.
def node_monitor(req):
    return render_to_response('monitor/node.html')
