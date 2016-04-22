#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response,RequestContext
from monitor.models import *
from cmdb.models import *
from game.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import sys,subprocess
import json
##编码
reload(sys)
sys.setdefaultencoding('utf8')


@login_required
def game_list(request):
	ipgroup_list = IpGroup.objects.all()
	kwvars = {
		'ipgroup_list':ipgroup_list,
		'login_user':request.user,
		'user_role':request.session.get('user_role'),
		}
	return render_to_response('game/game_list.html',kwvars,RequestContext(request))


def game_fun1(request):
	return HttpResponse("ok")
