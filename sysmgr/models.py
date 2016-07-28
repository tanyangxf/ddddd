#coding:utf-8
from django.db import models
import hashlib

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=254,verbose_name='用户名')
    password = models.CharField(max_length=256,verbose_name='密码')
    
    def __unicode__(self):
        return self.user_name
    def save(self,*args,**kwargs):
        self.password = hashlib.sha1(self.password+self.user_name).hexdigest()
        super(User,self).save(*args,**kwargs)