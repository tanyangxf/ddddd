from django.shortcuts import render_to_response,HttpResponse
from monitor.models import Host,User
from django.shortcuts import redirect

def host_mgr(req,page):
    try:
        page = int(page)
    except Exception,e:
        page = 1
    if req.method == 'POST':
        UserInput = req.POST
        host_name = UserInput['host_name']
        host_ip = UserInput['host_ip']
        host_ipmi = UserInput['host_ipmi']
        data_insert = Host(host_name=host_name,ip_addr=host_ip,ipmi_ip=host_ipmi)
        data_insert.save()
        return HttpResponse('ok')
    else:
        num = 5
        start = (page - 1)*num
        end = page*5
        total = Host.objects.all().count()
        all_result = Host.objects.all()[start:end]
        #divmod(14,5),result 2,4
        temp = divmod(total,num)
        if temp[1] == 0:
            all_page_count = temp[0]
        else:
            all_page_count = temp[0] + 1
        result_list = []
        for i in all_result:
            temp_dict = {}
            temp_dict['host_id'] = i.id
            temp_dict['host_name'] = i.host_name
            temp_dict['host_ip'] = i.ip_addr
            temp_dict['host_ipmi'] = i.ipmi_ip
            result_list.append(temp_dict)
        return render_to_response('sysmgr/host_mgr.html',
                                                            {'host_data':result_list,'all_page_count':range(all_page_count)})

def login(req):
    if req.method == 'POST':
        user_name = req.POST.get('username', None)
        password = req.POST.get('password', None)
        print user_name,password
        if user_name == 'ty' and password == 'ty':
            return redirect('/hpc/')
        else:
            return render_to_response('login.html', {'msg':'user_name or password is wrong!'})
    else:
        return render_to_response('login.html')
    
