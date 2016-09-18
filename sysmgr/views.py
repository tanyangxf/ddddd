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
        if host_name and host_ip:   
            data_insert = Host(host_name=host_name,host_ip=host_ip,host_ipmi=host_ipmi)
            print 'start'
            data_insert.save()
            print 'end'
            return HttpResponse('ok')
        else:
            
            return HttpResponse('failed')
    else:
        num = 12
        start = (page - 1)*num
        end = page*12
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
            temp_dict['host_ip'] = i.host_ip
            temp_dict['host_ipmi'] = i.host_ipmi
            result_list.append(temp_dict)
        return render_to_response('sysmgr/host_mgr.html',
                                                            {'host_data':result_list,'all_page_count':range(all_page_count)})

def login(req):
    if req.method == 'POST':
        user_name = req.POST.get('username', None)
        password = req.POST.get('password', None)
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
        if user_name and password:
            data_insert = User(user_name=user_name,password=password)
            data_insert.save()
            return HttpResponse('ok')
        else:
            return HttpResponse('failed')
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
        return render_to_response('sysmgr/user_mgr.html',{'user_data':result_list,'all_page_count':range(all_page_count)})

def del_user(req):
    if req.method == 'POST':
        user_num = req.POST.get('user_num',None)
        if user_num:
            for user_num in user_num.split(','):
                del_data = User.objects.get(id=user_num)
                del_data.delete()
            return HttpResponse('ok')

def modify_user(req):
    if req.method == 'POST':
        user_id = req.POST.get('user_id',None)
        user_name = req.POST.get('user_name',None)
        user_pass = req.POST.get('user_pass',None)       
        if user_name:
            row_data = User.objects.get(id=user_id)
            row_data.user_name = user_name
            #determine user password 
            if user_pass != 'notchange':
                row_data.password = user_pass
            row_data.save()
            return HttpResponse('ok')
    else:
        return HttpResponse('not change!')

def del_host(req):
    if req.method == 'POST':
        host_num = req.POST.get('host_num',None)
        if host_num:
            for host_num in host_num.split(','):
                del_data = Host.objects.get(id=host_num)
                del_data.delete()
            return HttpResponse('ok')
        else:
            return HttpResponse('failed')
        
def modify_host(req):
    if req.method == 'POST':
        host_id = req.POST.get('host_id',None)
        host_name = req.POST.get('host_name',None)
        host_ip = req.POST.get('host_ip',None)
        host_ipmi = req.POST.get('host_ipmi',None)
        if host_name and host_ip: 
            row_data = Host.objects.get(id=host_id)
            row_data.host_name = host_name
            row_data.host_ip = host_ip
            row_data.host_ipmi = host_ipmi
            row_data.save()
            return HttpResponse('ok')
    else:
        return HttpResponse('not change!')
