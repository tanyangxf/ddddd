#coding:utf-8
from django.db import models
import hashlib
# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=254,verbose_name=u'用户名',unique=True)
    password = models.CharField(max_length=254,verbose_name=u'用户密码')
    userid = models.IntegerField(verbose_name=u'用户ID',unique=True)
    user_group = models.CharField(max_length=254,verbose_name=u'用户组')
    other_group = models.CharField(max_length=254,verbose_name=u'附加组')
    user_home = models.CharField(max_length=254,verbose_name=u'用户主目录')
    user_type = models.CharField(max_length=20,verbose_name=u'用户类型')
    user_mail = models.CharField(max_length=50,verbose_name=u'用户邮件')
    user_tel = models.CharField(max_length=30,verbose_name=u'用户电话')
    user_comment = models.CharField(max_length=254,verbose_name=u'用户描述')
    is_login = models.CharField(max_length=10,verbose_name=u'是否能登录',default='True')
    
    def __unicode__(self):
        return self.user_name
    '''
        def save(self,*args,**kwargs):
            print self.user_name+self.password
            self.password = hashlib.sha512(self.password+self.user_name).hexdigest() 
            super(User,self).save(*args,**kwargs)
    '''
class Storage(models.Model):
    folder_name = models.CharField(max_length=254,verbose_name=u'设备名',unique=True)
    share_type = models.CharField(max_length=254,verbose_name=u'共享类型')
    share_parameter = models.CharField(max_length=254,verbose_name=u'共享参数')
    allow_ip = models.CharField(max_length=254,verbose_name=u'允许访问的ip')
    share_permission = models.CharField(max_length=254,verbose_name=u'共享权限')
    share_host = models.CharField(max_length=254,verbose_name=u'共享主机')