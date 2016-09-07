from django.shortcuts import render_to_response,HttpResponse
from monitor.models import Host
from django.shortcuts import redirect

# Create your views here.
def node_monitor(req):
    #host_data:
    #[{'host_name': u'test'}, {'host_name': u'ty.lan'}]
    node_data = Host.objects.values('host_name')
    if req.method == 'POST':
        return HttpResponse('ok')
    else:
        print "failed"
    return render_to_response('monitor/node.html',{'node_data':node_data})

