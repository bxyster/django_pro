#coding:utf8
from __future__ import unicode_literals

from django.db import models

class Hardware_info(models.Model):
	hostname = models.CharField(max_length=50)
	ip = models.GenericIPAddressField()
	osversion = models.CharField(max_length=50)
	memory = models.CharField(max_length=50)
	disk = models.CharField(max_length=50)
	vendor_id = models.CharField(max_length=50)
	model_name = models.CharField(max_length=50)
	cpu_core = models.CharField(max_length=50)
	product = models.CharField(max_length=50)
	Manufacturer = models.CharField(max_length=50)
	sn = models.CharField(max_length=100)

class IpGroup(models.Model):
	name = models.CharField(max_length=50)
	contents = models.CharField(max_length=100)
	def __unicode__(self):
		return self.name

class IpUsers(models.Model):
	auth_method_choices = (('ssh-password',"SSH/Password"),('ssh-key',"SSH/KEY"))
	auth_method = models.CharField(choices=auth_method_choices,max_length=16,help_text=u'如果选择SSH/KEY，请确保你的私钥文件已在settings.py中指定')
	username = models.CharField(max_length=32)
	password = models.CharField(max_length=64,blank=True,null=True,help_text=u'如果auth_method选择的是SSH/KEY,那此处不需要填写..')
	memo = models.CharField(max_length=128,blank=True,null=True)
	def __unicode__(self):
		return '%s(%s)' %(self.username,self.auth_method)

class IpManage(models.Model):
	name = models.CharField(max_length=50,default=True)
	ip = models.GenericIPAddressField()
	port = models.CharField(max_length=50,default='')
	group_name = models.ForeignKey('IpGroup')
	host_name = models.ForeignKey('IpUsers',default=True)
	hardware = models.ForeignKey('Hardware_info')
	def __unicode__(self):
		return self.name

class TaskManage(models.Model):
	result_choice = (
	(0,'等待执行'),
	(1,'正在执行'),
	(2,'已经执行'),
	(3,'执行失败'),
	(4,'执行成功'),
	)
	status_choice = (
	(0,'停用'),
	(1,'启用'),
	)
	type_choice = (
	(1,'命令执行'),
	(2,'脚本执行'),
	)
	name = models.CharField(max_length=50,default='')
	cron_type = models.CharField(max_length=10,choices=type_choice)
	cron_content = models.CharField(max_length=50)
	group_name = models.ForeignKey('IpGroup')
	cron_start_time = models.DateTimeField(blank=True,null=True)
	cron_end_time = models.DateTimeField(blank=True,null=True,default='')
	cron_total_time = models.CharField(max_length=10,blank=True,null=True)
	cron_result = models.CharField(max_length=10,choices=result_choice,default='0')
	cron_status = models.CharField(max_length=10,choices=status_choice,default='0')
	remark = models.CharField(max_length=100)
	def __unicode__(self):
		return self.name

class TaskDetail(models.Model):
	ip = models.GenericIPAddressField()
	task_cmds = models.CharField(max_length=50)
	task_result = models.CharField(max_length=300)
	task_id = models.ForeignKey('TaskManage')
	task_status = models.CharField(max_length=10)
	remark = models.CharField(max_length=100,blank=True,null=True)
	def __unicode__(self):
		return self.ip
