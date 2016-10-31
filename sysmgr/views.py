#coding:utf-8
from django.shortcuts import render_to_response,HttpResponse
from monitor.models import Host
from django.shortcuts import redirect
from django.template.context import RequestContext
from sysmgr.models import User
import commands
SHADOW_FILE = '/etc/shadow'
PASSWD_FILE = '/etc/passwd'
GROUP_FILE  = '/etc/group'


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
            data_insert.save()
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
                                  {'host_data':result_list,'all_page_count':range(all_page_count)},context_instance=RequestContext(req))


def user_mgr(req,page):
    try:
        page = int(page)
    except Exception:
        page = 1
    user_name_list = []
    #查询用户列表中id大于500的用户，如果不在用户列表，插入数据库
    with open(PASSWD_FILE) as pwd_file:
        #循环passwd文件中的每一行，
        for user_info in pwd_file.readlines():
            user_name = user_info.split(":",1)[0]
            user_name_list.append(user_name)
            userid = int(user_info.split(":",3)[2])
            if userid > 500 and userid < 5000:
                db_user = User.objects.filter(user_name=user_name).values('user_name')
                #如果用户在数据库中不存在，插入数据库
                if not db_user:
                    user_home = user_info.split(":",6)[5]
                    user_shell = user_info.split(":")[-1].split('/')[-1]
                    user_group = commands.getoutput('groups %s'%user_name).split(":")[1].strip()
                    is_login = 'True'
                    user_type = u'普通用户'
                    user_mail = ''
                    user_tel = ''
                    user_comment = ''
                    #查询用户密码
                    with open(SHADOW_FILE) as shadow_file:
                        for src in shadow_file.readlines():
                            shadow_user = src.split(':',1)[0]
                            if user_name == shadow_user:
                                password = src.split(':',2)[1]
                                if password == '!!' or user_shell.strip() == 'nologin': #用户是否能登录
                                    is_login = 'False'
                                elif password.startswith("!") and len(password) > 2 : #用户是否能登录
                                    is_login = 'False'
                    data_insert = User(user_name=user_name,userid=userid,password=password,user_home=user_home,
                                       user_group=user_group,user_type=user_type,user_mail=user_mail,user_tel=user_tel,
                                       user_comment=user_comment,is_login=is_login)
                    data_insert.save()
                #如果在数据库中存在，查询密码是否和数据库中一致
                else:
                    with open(SHADOW_FILE) as shadow_file:
                        for src in shadow_file.readlines():
                            shadow_user = src.split(':',1)[0]
                            #判断数据库用户和操作系统用户 ，对比密码
                            if db_user[0]['user_name'] == shadow_user:
                                #判断该用户的操作系统密码是否有问题
                                osuser_password = src.split(':',2)[1]
                                db_pass = User.objects.filter(user_name=user_name).values('password')
                                if db_pass[0]['password'] != osuser_password:
                                    #更新数据库中的密码，以防被更改
                                    data_update = User.objects.get(user_name=shadow_user)
                                    data_update.password = osuser_password
                                    data_update.save()
    #判断数据库中存在的用户在系统是否存在
    db_user = User.objects.values('user_name')
    for user in db_user:
        user_name = user.values()[0].strip()
        if user_name != 'superuser' and user_name not in user_name_list:
            del_data = User.objects.get(user_name=user_name)
            del_data.delete()

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
        temp_dict['userid'] = i.userid
        temp_dict['user_name'] = i.user_name
        temp_dict['user_home'] = i.user_home
        temp_dict['user_group'] = i.user_group
        temp_dict['user_type'] = i.user_type
        temp_dict['user_mail'] = i.user_mail
        temp_dict['user_tel'] = i.user_tel
        temp_dict['user_comment'] = i.user_comment
        temp_dict['is_login'] = i.is_login
        result_list.append(temp_dict)
    return render_to_response('sysmgr/user_mgr.html',{'user_data':result_list,'all_page_count':range(all_page_count)},
                              context_instance=RequestContext(req))

def create_user(req):
    if req.method == 'POST':
        UserInput = req.POST
        user_name = UserInput['user_name']
        password = UserInput['password']
        if user_name and password:
            data_insert = User(user_name=user_name,password=password)
            data_insert.save()
            return HttpResponse('ok')
        else:
            print 'failed'
            return HttpResponse('failed')
    else:
        return HttpResponse('failed')

def del_user(req):
    if req.method == 'POST':
        user_name = req.POST.get('user_name',None)
        if user_name:
            for user_name in user_name.split(','):
                commands.getoutput('userdel -r %s'%user_name)
                del_data = User.objects.get(user_name=user_name)
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
