#coding:utf8
import json  
import paramiko  

def curr_user_cmd(user_name,command):
    change_user = 'su - %s' %user_name 
    cmd = change_user + ' -c ' + ' ' + '"' + command + '"'
    return cmd

def curr_user_job_cmd(user_name,command):
    change_user = 'su  %s' %user_name 
    cmd = change_user + ' -c ' + ' ' + '"' + command + '"'
    return cmd
  
def connect(host,user_name):  
    'this is use the paramiko connect the host,return conn'  
    ssh = paramiko.SSHClient()  
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    try:  
#        ssh.connect(host,username='root',allow_agent=True,look_for_keys=True)  
        ssh.connect(host,username=user_name,allow_agent=True,timeout=1)  
        return ssh  
    except:
        return None
  
def command(args,outpath):  
    'this is get the command the args to return the command'  
    cmd = '%s %s' % (outpath,args)  
    return cmd  
  
def exec_commands(conn,cmd):  
    'this is use the conn to excute the cmd and return the results of excute the command'  
    if not conn:
        return ('','failed')
    stdin,stdout,stderr = conn.exec_command(cmd)  
    results=stdout.read()
    err = stderr.read()  
    if err:
        err = 'failed'
    return results,err
  
def excutor(host,outpath,args):  
    conn = connect(host)  
    if not conn:  
        return [host,None]  
    #exec_commands(conn,'chmod +x %s' % outpath)  
    cmd =command(args,outpath)  
    result = exec_commands(conn,cmd)  
    result = json.dumps(result)  
    return [host,result]  
def upload_module(conn,inpath,outpath):  
    'this is upload the module to the remote server'  
    ftp = conn.open_sftp()  
    ftp.put(inpath,outpath)  
    ftp.close()  
    return outpath   

def download_module(conn,inpath,outpath):  
    'this is download the module to the remote server'  
    ftp = conn.open_sftp()  
    ftp.get(inpath,outpath)  
    ftp.close()  
    return outpath
  
  
if __name__ == '__main__':  
    pass
    #print json.dumps(excutor('192.168.1.165','ls',' -l'),indent=4,sort_keys=True)  
    #print curr_user_exec('tanyang', 'ls /home')
    #upload_module(connect('172.16.123.1','tanyang'),'views.py','/Users/tanyang/4.sh')  
    #download_module(connect('172.16.123.1','tanyang'),'4.sh','/root/5.sh')
    #print exec_commands(connect('127.0.0.1','tanyang'),'/usr/local/bin/gls -la --time-style %s %s ' % ("'+%Y/%m/%d %H:%M:%S'",'/Users/tanyang/yicloud/'))
