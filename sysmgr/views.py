#coding:utf-8
from django.shortcuts import render_to_response,HttpResponse
from monitor.models import Host
from django.shortcuts import redirect
from sysmgr.models import User
import hashlib

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
        user_name = str(req.POST.get('username', None))
        password = str(req.POST.get('password', None))
        password = hashlib.sha1(password+user_name).hexdigest()
        #name = User.objects.get(user_name = user_name).user_name
        user = User.objects.filter(user_name=user_name,password=password)
        if user:
            name = User.objects.get(user_name = user_name).user_name
            return redirect("/hpc")
        else:
            return render_to_response('login.html', {'msg':'用户名或密码错误'})
    else:
        return render_to_response('login.html')

def user_mgr(req,page):
    try:
        page = int(page)
    except Exception,e:
        page = 1
    if req.method == 'POST':
        UserInput = req.POST
        user_name = UserInput['user_name']
        password = UserInput['password']
        data_insert = User(user_name=user_name,password=password)
        data_insert.save()
        return HttpResponse('ok')
    else:
        num = 5
        start = (page - 1)*num
        end = page*5
        total = User.objects.all().count()
        all_result = User.objects.all()[start:end]
        #divmod(14,5),result 2,4
        temp = divmod(total,num)
        if temp[1] == 0:
            all_page_count = temp[0]
        else:
            all_page_count = temp[0] + 1
        result_list = []
        for i in all_result:
            temp_dict = {}
            temp_dict['user_id'] = i.id
            temp_dict['user_name'] = i.user_name
            result_list.append(temp_dict)
        return render_to_response('sysmgr/user_mgr.html',
                                                            {'user_data':result_list,'all_page_count':range(all_page_count)})

