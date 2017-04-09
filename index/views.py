#coding:utf-8
from django.shortcuts import render
from django.shortcuts import redirect
from sysmgr.models import User
from django.db.models import Sum
from clusmgr.remote_help import curr_user_cmd
import commands
import json
import crypt
import hashlib
from job.models import Job_list
from monitor.models import *
from django.http.response import HttpResponse
from config.config import *

def default(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect('/login')
    user_name = user_dict['user_name']
    if user_name == 'root':
        return render(req,'admin_default.html',{'user_name':user_name})
    else:
        return render(req,'normal_default.html',{'user_name':user_name})

def login(req):
    if req.method == 'POST':
        try:
            user_name = req.POST.get('username', None)
            input_password = req.POST.get('password', None)
            if not user_name and not input_password:
                return render(req,'login.html', {'msg':'用户名和密码不能为空'})
            elif not user_name and input_password:
                return render(req,'login.html', {'msg':'用户名不能为空'})
            elif user_name and not input_password:
                return render(req,'login.html', {'msg':'密码不能为空'})
            if user_name == 'superuser':
                input_password = hashlib.sha512(input_password+user_name).hexdigest() 
                db_pass = User.objects.get(user_name=user_name).password
                if input_password == db_pass:
                    user_name = 'root'
                    req.session['is_login'] = {'user_name': user_name}
                    return redirect("/")
                else:
                    return render(req,'login.html', {'msg':'用户名或密码错误'})
            #匹配passwd文件中的用户名
            with open(PASSWD_FILE) as pwd_file:
                for user_info in pwd_file.readlines():
                    userid = int(user_info.split(":",3)[2])
                    #判断用户id大于500并且小于5000的用户
                    if userid > 500 and userid < 5000:
                        os_user_name = user_info.split(":",1)[0]
                        #如果登录用户在系统存在
                        if user_name == os_user_name:
                            #判断用户shell
                            user_shell = user_info.split(":")[-1].split('/')[-1]
                            if user_shell.strip() == 'nologin':
                                return render(req,'login.html', {'msg':'用户登已禁用'})
                            db_user = User.objects.filter(user_name=user_name).values('user_name')
                            #如果用户在数据库中不存在，插入数据库
                            if not db_user:
                                with open(SHADOW_FILE) as shadow_file:
                                    for src in shadow_file.readlines():
                                        shadow_user = src.split(':',1)[0]
                                        #如果在操作系统中存在用户 ，对比密码
                                        if user_name == shadow_user:
                                            #判断该用户的操作系统密码是否有问题
                                            try:
                                                osuser_password = src.split(':',2)[1]
                                                start_index=osuser_password.find("$")  #找到第一个“$”出现的索引
                                                finish_index=osuser_password.rfind("$") #找到最后一个“$”出现的索引
                                                salt=osuser_password[start_index:finish_index+1] #两个$之间的为盐
                                            except:
                                                return render(req,'login.html', {'msg':'系统错误！'})
                                            if osuser_password == '!!': #判断密码是否为空
                                                return render(req,'login.html', {'msg':'用户名或密码错误'})
                                            elif osuser_password.startswith("!") and len(osuser_password) > 2:
                                                return render(req,'login.html', {'msg':'用户登已禁用'})
                                            #判断用户输入密码和操作系统密码是否匹配
                                            elif crypt.crypt(input_password,salt) == osuser_password:
                                                user_home = user_info.split(":",6)[5]
                                                #user_group = commands.getoutput('groups %s'%user_name).split(":")[1].strip()
                                                group_result = commands.getoutput('id -Gn %s'%user_name).split(' ',1)
                                                user_group = group_result[0]
                                                if len(group_result) == 1:
                                                    other_group = ''
                                                else:
                                                    other_group = group_result[1]
                                                is_login = 'True'
                                                user_type = u'普通用户'
                                                user_mail = ''
                                                user_tel = ''
                                                user_comment = ''
                                                data_insert = User(user_name=user_name,userid=userid,password=osuser_password,user_home=user_home,
                                                                   user_group=user_group,other_group=other_group,user_type=user_type,user_mail=user_mail,user_tel=user_tel,
                                                                   user_comment=user_comment,is_login=is_login)
                                                data_insert.save()
                                                req.session['is_login'] = {'user_name': user_name}
                                                return redirect("/")
                            #如果用户在数据库中存在,判断密码
                            else:
                                is_login = User.objects.filter(user_name=user_name).values('is_login')[0]['is_login']
                                if is_login == 'False':
                                    return render(req,'login.html', {'msg':'用户登已禁用'})
                                with open(SHADOW_FILE) as shadow_file:
                                    for src in shadow_file.readlines():
                                        shadow_user = src.split(':',1)[0]
                                        #如果在操作系统中存在用户 ，对比密码
                                        if user_name == shadow_user:
                                            #判断该用户的操作系统密码是否有问题
                                            osuser_password = src.split(':',2)[1]
                                            start_index=osuser_password.find("$")  #找到第一个“$”出现的索引
                                            finish_index=osuser_password.rfind("$") #找到最后一个“$”出现的索引
                                            salt=osuser_password[start_index:finish_index+1] #两个$之间的为盐
                                            if osuser_password == '!!': #判断密码是否为空
                                                return render(req,'login.html', {'msg':'用户名或密码错误'})
                                            elif osuser_password.startswith("!") and len(osuser_password) > 2:
                                                return render(req,'login.html', {'msg':'用户登已禁用'})
                                            elif crypt.crypt(input_password,salt) == osuser_password:
                                                #更新数据库中的密码，以防被认为更改
                                                data_update = User.objects.filter(user_name=user_name)
                                                data_update.update(password = osuser_password)
                                                req.session['is_login'] = {'user_name': user_name}
                                                return redirect("/")
        except Exception,e:
            print e
            return render(req,'login.html', {'msg':'系统错误！'})          
        return render(req,'login.html', {'msg':'用户名或密码错误'})                           
    else:
        return render(req,'login.html')
def logout(req):
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    del req.session['is_login']
    return render(req,'login.html')
    
def index(req):
    req.session.set_expiry(1800)
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return redirect("/login")
    user_name = user_dict['user_name']
    try:
        #get pbs nodes status
        pbs_all_nodes = int(commands.getoutput(PESTAT + '|wc -l')) - 1
    except Exception,e:
        print 'error is %s' %e
        pbs_all_nodes = ''
    try:
        #pbs_free_nodes = commands.getoutput('pbsnodes -l free|wc -l')
        pbs_down_nodes = int(commands.getoutput(PBSNODES + ' -l down|wc -l'))
        pbs_offline_nodes = int(commands.getoutput(PBSNODES + ' -l offline|wc -l'))
        pbs_unknown_nodes = int(commands.getoutput(PBSNODES + ' -l state-unknown|wc -l'))
        pbs_free_nodes = pbs_all_nodes - pbs_down_nodes - pbs_offline_nodes - pbs_unknown_nodes
    except Exception,e:
        pbs_down_nodes = ''
        pbs_offline_nodes = ''
        pbs_unknown_nodes = ''
        pbs_free_nodes = ''
        
    cluster_status = {'pbs_all_nodes':pbs_all_nodes,'pbs_free_nodes':pbs_free_nodes,
                      'pbs_down_nodes':pbs_down_nodes,'pbs_offline_nodes':pbs_offline_nodes,
                      'pbs_unknown_nodes':pbs_unknown_nodes}
    try:
        #get pbs queue status
        cmd = commands.getoutput(QSTAT +' -Q')
        queue_temp_list = cmd.split('\n')[2:]
        queue_dict = {}
        for queue in queue_temp_list:
            temp_queue_list = []
            queue_name = str(queue.split()[0])
            queue_max_run = int(queue.split()[1])
            queue_run_job = int(queue.split()[6])
            temp_queue_list.append(queue_max_run)
            temp_queue_list.append(queue_run_job)
            queue_dict[queue_name] = temp_queue_list
        cluster_status['queue_status'] = json.dumps(queue_dict)
    except:
        cluster_status['queue_status'] = ''
    
    try:
        #获取集群cpu状态信息
        '''
        {'l_cpu_count__sum': 6}
        {'cpu_percent__sum': 13.5}
        '''
        l_cpu_count = Cpu.objects.aggregate(Sum('l_cpu_count'))
        all_cpu_percent = Cpu.objects.aggregate(Sum('cpu_percent'))
        #转换字典，添加到cluster_status字典
        cluster_status = dict(cluster_status,**l_cpu_count)
        cluster_status = dict(cluster_status,**all_cpu_percent)
        return render(req,"index.html",cluster_status)
    except Exception:
        return render(req,"index.html",cluster_status)
    
def get_session(req):
    user_dict = req.session.get('is_login', None)
    if not user_dict:
        return HttpResponse('no data')
    return HttpResponse('ok')