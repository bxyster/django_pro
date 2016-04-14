#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response,RequestContext
from monitor.models import *
from cmdb.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import sys,subprocess
import json
##编码
reload(sys)
sys.setdefaultencoding('utf8')
#定义初始值
tmp_time = 0

@login_required
def monitor_view(request,m):
	if request.method == "POST":
		ip_name_list = IpManage.objects.filter(group_name=m)
		host_name = []
		host_id = []
		for i in ip_name_list:
			host_name.append(i.name)
			host_id.append(i.id)
		dict_name = dict(zip(host_name,host_id))
		kwvars = {
			'dict_name':dict_name,
		}
		return HttpResponse(json.dumps(kwvars))
	return HttpResponse('no data')

@login_required
def monitor(request):
	ipgroup_list = IpGroup.objects.all()
	kwvars = {
		'ipgroup_list':ipgroup_list,
		'login_user':request.user,
		'user_role':request.session.get('user_role'),
		}
	return render_to_response('monitor/monitor.html',kwvars,RequestContext(request))

@login_required
def monitor_graph(request):
	global tmp_time
	if tmp_time>0:
		mem = Mem.objects.filter(mem_times__gt='%s'% str(tmp_time/1000))
	else:
		mem = Mem.objects.all()
	mem = Mem.objects.all()
	arr = []
	for i in mem:
		arr.append([int(i.mem_times)*1000,int(i.mem_values)])
	if len(arr)>0:
		tmp_time = arr[-1][0]
	return HttpResponse(json.dumps(arr))

@login_required
def monitor_cpu_graph(request,c_type):
	cpu_min = cpu_load_info.objects.filter(cpu_type=c_type)
	arr_cpu = []
	for i in cpu_min:
		arr_cpu.append([int(i.info_times)*1000,float(i.cpu_loads_val)])
	return HttpResponse(json.dumps(arr_cpu))

@login_required
def monitor_zabbix(request):
	ipgroup_list = IpGroup.objects.all()
	kwvars = {
		'ipgroup_list':ipgroup_list,
		'login_user':request.user,
		'user_role':request.session.get('user_role'),
		}
	return render_to_response('monitor/monitor_zabbix.html',kwvars,RequestContext(request))

@login_required
def alarm(request):
	kwvars = {
		'login_user':request.user,
		'user_role':request.session.get('user_role'),
		}
	return render_to_response('monitor/alarm.html',kwvars,RequestContext(request))
