#!/usr/bin/env python
#coding:utf8
import hashlib,time
from django.http import HttpResponse

def api_auth(func):
	def wrapper(request):
		securty_key = request.META.get('HTTP_SECURTYKEY',None)
		print "这里是获取客户端的加密",securty_key
		if not securty_key:
			return HttpResponse('密钥为空')
		if not auth_api_valid(securty_key):
			return HttpResponse('密钥错误')
		return func(request)
	return wrapper

def auth_api_valid(data):
	try:
		encrytion,time_span = data.split('/')
		time_span = float(time_span)
		if (time.time() - time_span) > 5:
			return Fasle
		hash_obj = hashlib.md5()
		key = '&W0@6M9HXm05viBx'
		hash_obj.update('%s/%f' % (key,time_span))
		print "这里是服务器上解密",hash_obj.hexdigest()
		if hash_obj.hexdigest() == encrytion:
			return True
		else:
			return False
	except Exception,e:
		pass
	return False
