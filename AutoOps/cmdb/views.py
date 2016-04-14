#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response,RequestContext
from cmdb.models import *
from django.views.decorators.csrf import csrf_exempt
from api_auth import api_auth
from django.contrib.auth.decorators import login_required
import sys,subprocess
import json
##编码
reload(sys)
sys.setdefaultencoding('utf8')
# Create your views here.

@csrf_exempt
@api_auth
def hardwareinfo(req):
	if req.method == 'POST':
		hostname = req.POST.get('hostname')
		ip = req.POST.get('ip')
		osversion = req.POST.get('osversion')
		memory = req.POST.get('memory')
		disk = req.POST.get('disk')
		vendor_id = req.POST.get('vendor_id')
		model_name = req.POST.get('model_name')
		cpu_core = req.POST.get('cpu_core')
		product = req.POST.get('product')
		Manufacturer = req.POST.get('Manufacturer')
		sn = req.POST.get('sn')
		try:
			host = Hardware_info.objects.get(hostname=hostname)
		except:
			host = Hardware_info()
		host.hostname = hostname
		host.ip = ip
		host.osversion = osversion
		host.memory = memory
		host.disk = disk
		host.vendor_id = vendor_id
		host.model_name = model_name
		host.cpu_core = cpu_core
		host.product = product
		host.Manufacturer = Manufacturer
		host.sn = sn
		host.save()
		return HttpResponse('all done')
	else:
		return HttpResponse('no data')


@login_required
def assets_list(request):
	Getassets = Hardware_info.objects.all()
	kwvars = {
		'login_user':request.user,
		'Getassets':Getassets,
		'user_role':request.session.get('user_role'),
		}
	return render_to_response('cmdb/assets_list.html',kwvars,RequestContext(request))

@login_required
def ipgroup_list(request):
	Getipgroup = IpGroup.objects.all()
	kwvars = {
		'login_user':request.user,
		'Getipgroup':Getipgroup,
		'user_role':request.session.get('user_role'),
		}
	return render_to_response('cmdb/ipgroup_list.html',kwvars,RequestContext(request))

@login_required
def ip_list(request):
	Getipmanage = IpManage.objects.all()
	kwvars = {
		'login_user':request.user,
		'Getipmanage':Getipmanage,
		'user_role':request.session.get('user_role'),
		}
	return render_to_response('cmdb/ip_list.html',kwvars,RequestContext(request))


@login_required
def multi_cmd(request):
	result = ''
	count_ip = 0 
	success_ip = 0
	failed_ip = 0
	iplists = []
	if request.method == 'POST':
		exec_type = request.POST.get('exec_type')
		ipid_list = request.POST.getlist('iplist')
		groups_id = request.POST.getlist('ipgrouplist')
		cmd_name = request.POST.get('cmd_name')
		if exec_type == 'ip_list':
			for id in ipid_list:
				if 'multiselect-all' not in id:
					ip_id = IpManage.objects.get(id=id)
					iplists.append(int(ip_id.id))
		else:
			for id in groups_id:
				if 'multiselect-all' not in id:
					group_names = IpGroup.objects.filter(id=id)
					for names in group_names:
						ip_lists = IpManage.objects.filter(group_name=names)
						for id in ip_lists:
							ip = IpManage.objects.get(id=id.id)
							iplists.append(int(ip.id))
		count_ip = len(iplists)
		result = subprocess.Popen("python backend/multitask.py '-task_type' 'cmd' '-task_list' \
		'%s' '-expire' '30' '-task' '%s' '-uid' '1'"% (iplists,cmd_name),shell = True,stdout=subprocess.PIPE)
		result = result.stdout.readlines()
		result = ''.join(result)
		result = result.replace('\n','<br>')
		success_ip = result.count('=End=')
		failed_ip = int(count_ip)-int(success_ip)
	IpGrouplist = IpGroup.objects.all()
	Iplist = IpManage.objects.all()
	kwvars = {
		'Iplist':Iplist,
		'count_ip':count_ip,
		'failed_ip':failed_ip,
		'success_ip':success_ip,
		'result':result,
		'IpGrouplist':IpGrouplist,
        'login_user':request.user,
        'user_role':request.session.get('user_role'),
	}
	return render_to_response('cmdb/multi_cmd.html',kwvars,RequestContext(request))

@login_required
def multi_file(request):
	IpGrouplist = IpGroup.objects.all()
	kwvars = {
		'IpGrouplist':IpGrouplist,
        'login_user':request.user,
        'user_role':request.session.get('user_role'),
	}
	return render_to_response('cmdb/multi_file.html',kwvars,RequestContext(request))

@login_required
def multi_info_collect(request):
	iplists = []
	result = '' 
	if request.method == 'POST':
		exec_type = request.POST.get('exec_type')
		ipid_list = request.POST.getlist('iplist')
		groups_id = request.POST.getlist('ipgrouplist')
		exec_cmds = request.POST.get('exec_cmds')
		if exec_cmds == 'exec_post_info':
			cmd_name = 'python /data/web/AutoOps/scripts/post_hardware.py'
		else:
			cmd_name = ''
		if exec_type == 'ip_list':
			for id in ipid_list:
				if 'multiselect-all' not in id:
					ip_id = IpManage.objects.get(id=id)
					iplists.append(int(ip_id.id))
		else:
			for id in groups_id:
				if 'multiselect-all' not in id:
					group_names = IpGroup.objects.filter(id=id)
					for names in group_names:
						ip_lists = IpManage.objects.filter(group_name=names)
						for id in ip_lists:
							ip = IpManage.objects.get(id=id.id)
							iplists.append(int(ip.id))
		count_ip = len(iplists)
		result = subprocess.Popen("python backend/multitask.py '-task_type' 'cmd' '-task_list' \
		'%s' '-expire' '30' '-task' '%s' '-uid' '1'"% (iplists,cmd_name),shell = True,stdout=subprocess.PIPE)
		result = result.stdout.readlines()
		result = ''.join(result)
		result = result.replace('\n','<br>')
		success_ip = result.count('=End=')
		failed_ip = int(count_ip)-int(success_ip)
	IpGrouplist = IpGroup.objects.all()
	Iplist = IpManage.objects.all()
	kwvars = {
		'result':result,
		'Iplist':Iplist,
		'IpGrouplist':IpGrouplist,
        'login_user':request.user,
        'user_role':request.session.get('user_role'),
	}
	return render_to_response('cmdb/multi_info_collect.html',kwvars,RequestContext(request))

@login_required
def task_detail(request,id):
	taskdata = TaskDetail.objects.filter(task_id=id)
	kwvars = {
		'taskdata':taskdata,
        'login_user':request.user,
        'user_role':request.session.get('user_role'),
	}
	return render_to_response('cmdb/task_detail.html',kwvars,RequestContext(request))

@login_required
def task_add(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		cron_type = request.POST.get('cron_type')
		cron_content = request.POST.get('cron_content')
		group_id = request.POST.get('group_id')
		group_name = IpGroup.objects.get(id=group_id)
		cron_start_time = request.POST.get('cron_start_time')
		remark = request.POST.get('remark')
		if request.session.get('user_role') == 3:
			return HttpResponse(u"普通用户没有权限!!!")
		elif TaskManage.objects.filter(name=name):
			return HttpResponse("任务名称重复")
		taskmanage = TaskManage(name=name,cron_type=cron_type,cron_content=cron_content,\
		group_name=group_name,cron_start_time=cron_start_time,remark=remark)
		taskmanage.save()
		return HttpResponse("保存完毕")
	IpGrouplist = IpGroup.objects.all()
	task_list = TaskManage.objects.all().order_by("-cron_start_time")
	kwvars = {
		'IpGrouplist':IpGrouplist,
		'task_list':task_list,
		'login_user':request.user,
		'user_role':request.session.get('user_role'),
	}
	return render_to_response('cmdb/task_add.html',kwvars,RequestContext(request))

@login_required
def task_del(request,id):
	if request.session.get('user_role') == 3:
		return HttpResponse(u"普通用户没有权限!!!")
	taskmanage = TaskManage.objects.get(id=id)
	if taskmanage.cron_status == '1':
		taskmanage.cron_status = 0
		taskmanage.save()
	elif taskmanage.cron_status == '0':
		taskmanage.cron_status = 1
		taskmanage.save()
	return HttpResponse('修改成功')
	

@login_required
def task_modify(request,id):
	if request.method == 'GET':
		taskmanage = TaskManage.objects.get(id=id)
		kwvars = {
		'id':taskmanage.id,
		'name':taskmanage.name,
		'task_type':taskmanage.cron_type,
		'task_content':taskmanage.cron_content,
		'cron_start_time':taskmanage.cron_start_time.strftime('%Y-%m-%d %H:%M:%S'),
		'task_remark':taskmanage.remark,
		}
		return HttpResponse(json.dumps(kwvars))
	if request.method == 'POST':
		task = TaskManage.objects.get(id=id)
		name = request.POST.get('task_name')
		cron_type = request.POST.get('task_type')
		cron_content = request.POST.get('task_content')
		group_id = request.POST.get('group_id')
		group_name = IpGroup.objects.get(id=group_id)
		cron_start_time = request.POST.get('task_start_time')
		remark = request.POST.get('task_remark')
		if request.session.get('user_role') == 3:
			return HttpResponse(u"普通用户没有权限!!!")
		task.name = name
		task.cron_content = cron_content
		task.cron_type = cron_type
		task.group_name = group_name
		task.cron_start_time = cron_start_time
		task.remark = remark
		task.save()
		return HttpResponse("修改完毕")
	IpGrouplist = IpGroup.objects.all()
	task_list = TaskManage.objects.all()
	kwvars = {
		'IpGrouplist':IpGrouplist,
		'task_list':task_list,
		'login_user':request.user,
		'user_role':request.session.get('user_role'),
	}
	return render_to_response('cmdb/task_add.html',kwvars,RequestContext(request))

@login_required
def ip_user(request):
	Ipusers = IpUsers.objects.all()
	kwvars = {
		'login_user':request.user,
		'Ipusers':Ipusers,
		'user_role':request.session.get('user_role'),
		}
	return render_to_response('cmdb/ip_user.html',kwvars,RequestContext(request))

@login_required
def manual(request):
	subprocess.call("python cron/task.py",shell = True,stdout=subprocess.PIPE)
	return HttpResponse('执行成功')
