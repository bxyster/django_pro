#coding:utf8

from django.http import HttpResponseRedirect
import os



list_role = {
	1:"超级管理员",
	2:"系统管理员",
	3:"普通用户",
}


def is_user(fun):
	def result(*arg,**kwargs):
		if request.session.get('user_role') == 3:
			return HttpResponse(u"普通用户没有权限!!!")
		fun()
	return result
