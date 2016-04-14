#coding:utf8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from account.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
import datetime
import sys,json
import get_client_ip
from backend import role_control
##编码
reload(sys)
sys.setdefaultencoding('utf8')

#保存日志
def save_log(request,result,msg):
	user = request.session.get('user_name')
	ip = get_client_ip.get_client_ip(request)
	msg = msg
	result = result
	logdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	ywlog = YwLog(user=user,ipaddress=ip,msg=msg,result=result,logdate=logdate)
	ywlog.save()


#验证登录
def login_user(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = auth.authenticate(username=username,password=password)
		if user and user.is_active:
			auth.login(request,user)
	#		request.session.set_expiry(60*30)
			request.session['user_name'] = user.username
			request.session['user_role'] = user.role
			request.session['user_id'] = user.id
			save_log(request,1,'登录系统')
			return HttpResponseRedirect('/')
		else:
			user = username 
			ip = get_client_ip.get_client_ip(request)
			msg = '登录系统'
			result = 0
			logdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			ywlog = YwLog(user=user,ipaddress=ip,msg=msg,result=result,logdate=logdate)
			ywlog.save()
			return render_to_response('account/login.html',{'login_err': '当前登录用户不存在或密码错误!'},RequestContext(request))
	else:
		return render_to_response('account/login.html',RequestContext(request))

#登出
def logout_user(request):
	save_log(request,1,'登出系统')
	auth.logout(request)
	return HttpResponseRedirect("/")

#首页
@login_required
def index(request):
	user_id = request.session.get('user_id')
	kwvars = {
		'user_id':user_id,
		'login_user':request.user,
		'user_role':request.session.get('user_role'),
	}
	return render_to_response('index.html',kwvars)


#用户列表
@login_required
def account_list(request):
	GetUser = User.objects.all()
	GetDept = Dept.objects.all()
	user_id = request.session.get('user_id')
	kwvars = {
		'login_user':request.user,
		'GetUser':GetUser,
		'dep_list':GetDept,
		'list_role':role_control.list_role,
		'user_id':user_id,
		'user_role':request.session.get('user_role'),
	}
	return render_to_response('account/account_list.html',kwvars,RequestContext(request))

#用户增加
@login_required
def account_add(request):
	if request.session.get('user_role') == 3:
		save_log(request,0,'用户新增')
		return HttpResponse('no_permission')
	if request.method == 'POST':
		user_name = request.POST.get('user_name')
		nick_name = request.POST.get('nick_name')
		email_name = request.POST.get('email_name')
		phone = request.POST.get('phone')
		dept_id = request.POST.get('dept_name')
		dept_name = Dept.objects.get(id=dept_id)
		role_id = request.POST.get('role_name')
		isactive = request.POST.get('isactive')
		password = request.POST.get('password')
		password = make_password(password)
		sex_name = request.POST.get('sex_name')
		if User.objects.filter(username=user_name):
			return HttpResponse('username_exit')
		elif User.objects.filter(nickname=nick_name):
			return HttpResponse('name_exit')
		else:
			user_info = User(username=user_name,password=password,nickname=nick_name,email=email_name,phone=phone,\
			is_active=isactive,sex=sex_name,role=role_id,dept=dept_name)
			user_info.save()
			save_log(request,1,'用户新增')
			return HttpResponse('ok')
#用户删除
@login_required
def account_del(request,num):
	if request.session.get('user_role') == 3:
		save_log(request,0,'用户删除')
		return HttpResponse(u"普通用户没有权限!!!")
	elif num == '1':
		save_log(request,0,'用户删除')
		return HttpResponse(u'超级管理员不能删除')
	else:
		get_user_model().objects.get(id=num).delete()
	save_log(request,1,' 用户删除')
	return HttpResponse('ok')



#用户编辑
@login_required
def account_edit(request,id):
	if request.method == 'GET':
		Userinfo = User.objects.filter(id=id)
		Username = request.session.get('user_name')
		Deptlist = Dept.objects.all()
		user_id = request.session.get('user_id')
		kwvars = {
			'user_id':user_id,
			'login_user':request.user,
		    'Userinfo': Userinfo,
		    'list_role': role_control.list_role,
		    'Deptlist': Deptlist,
		    'username': Username,}
		return render_to_response('account/account_edit.html',kwvars,RequestContext(request))
	if request.method == 'POST':
		if request.session.get('user_role') == 3:
			save_log(request,0,'用户编辑')
			return HttpResponse(u"普通用户没有权限!!!")
		Useredit =User.objects.get(id=id)
		Useredit.username = request.POST.get('username')
		Useredit.email = request.POST.get('email')
		Useredit.sex = request.POST.get('sex')
		dept = request.POST.get('dept')
		Useredit.dept = Dept.objects.get(id=dept)
		Useredit.nickname = request.POST.get('nickname')
		Useredit.phone = request.POST.get('phone')
		Useredit.role = request.POST.get('role') 
		Useredit.is_active = int(request.POST.get('isactive')) 
		Useredit.save()
		save_log(request,1,'用户修改')
		return HttpResponse(u"用户修改成功")	

#用户查看
@login_required
def account_detail(request,id):
	user_id = request.session.get('user_id')
	Userdata = User.objects.filter(id=id)
	GetDept = Dept.objects.all()
	kwvars = {
		'user_id':user_id,
		'login_user':request.user,
		'Userdata':Userdata,
		'dep_list':GetDept,
		'list_role':role_control.list_role,
		'user_role':request.session.get('user_role'),
	}
	return render_to_response('account/account_detail.html',kwvars,RequestContext(request))

#修改密码
@login_required
def setpasswd(request,id):
	Userinfo = request.session.get('user_name')
	Adminrole=User.objects.get(username=Userinfo)
	Uid = Adminrole.role
	user_id = request.session.get('user_id')	
	if request.method == 'GET':
		UserDATA=User.objects.get(id=id)
		kwvars = {
			'user_id':user_id,
			'login_user':request.user,
	        'username': Userinfo,
	        'UserDAT': UserDATA,
	        'ID': Uid,
		}
		return render_to_response('account/setpasswd.html', kwvars ,RequestContext(request))
	if request.method == 'POST':
		if request.session.get('user_role') != 1:
			save_log(request,0,'修改密码')
			return HttpResponse(u"超级管理员才可修改密码")
		Userset =User.objects.get(id=id)
		if not Uid ==1:    #如果不是用户超级管理员就进行验证
			oldpasswd=request.POST.get('oldpasswd')   #判断用户输入的当前密码是否正确
			if not Userset.check_password(oldpasswd):
				save_log(request,0,'修改密码')
				return HttpResponse(u"输入的原密码不正确")
		passwd1= request.POST.get('newpasswd1')
		passwd2= request.POST.get('newpasswd2')
		if not passwd2 == passwd1:
			save_log(request,0,'修改密码')
			return HttpResponse(u"您输入的密码不一致!!!!!")
		else:
			Userset.set_password(passwd1)
			Userset.save()
			save_log(request,1,'修改密码')
			return HttpResponse(u"密码修改成功")


#用户组列表
@login_required
def dep_list(request):
	GetDept = Dept.objects.all()
	user_id = request.session.get('user_id')
	kwvars = {
		'user_id':user_id,
		'login_user':request.user,
		'GetDept':GetDept,
		'user_role':request.session.get('user_role'),
	}
	return render_to_response('account/dep_list.html',kwvars)


#日志列表
@login_required
def log_list(request):
	log_list = YwLog.objects.all().order_by('-logdate')
	user_id = request.session.get('user_id')
	kwvars = {
		'user_id':user_id,
		'login_user':request.user,
		'log_list':log_list,
		'user_role':request.session.get('user_role'),
	}
	return render_to_response('account/logging.html',kwvars)

