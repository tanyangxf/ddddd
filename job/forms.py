#coding:utf-8
from django import forms
class Login(forms.Form):
    username = forms.CharField(label=("Username"), max_length=254)
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput)

class New_Job(forms.Form):
    job_name = forms.CharField(label=("Job_name"), max_length=254)
    job_cpu  = forms.IntegerField(label=("Job_cpu"))
    job_command = forms.CharField(label=("Job_command"))

class Job_mgr(forms.Form):
    command = forms.CharField(label=(u'系统命令'), max_length=254)