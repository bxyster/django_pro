#!/usr/bin/env python
#coding=utf-8
import json
import urllib2
import sys
 
##########################
class Zabbix:
	def __init__(self):
		self.url = "http://192.168.52.6/api_jsonrpc.php"
		self.header = {"Content-Type": "application/json"}
		self.authID = self.user_login()
	#验证登录
	def user_login(self):
		data = json.dumps({
	                        "jsonrpc": "2.0",
	                        "method": "user.login",
	                        "params": {"user": "admin",   "password": "zabbix"},
	                        "id": 0})
		request = urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key,self.header[key])
		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			print "Auth Failed, Please Check Your Name And Password:",e.code
		else:
			response = json.loads(result.read())
			result.close()
			authID = response['result']
			return authID
	#通用调用接口
	def get_data(self,data,hostip=""):
		request = urllib2.Request(self.url,data)
		for key in self.header:
			request.add_header(key,self.header[key])
		try:
			result = urllib2.urlopen(request)
		except URLError as e:
			if hasattr(e, 'reason'):
				print 'We failed to reach a server.'
				print 'Reason: ', e.reason
			elif hasattr(e, 'code'):
				print 'The server could not fulfill the request.'
				print 'Error code: ', e.code
				return 0
		else:
			response = json.loads(result.read())
			result.close()
			return response

	#获取所有主机和对应的hostid
	def hostsid_get(self):
		data = json.dumps({
		                    "jsonrpc": "2.0",
		                    "method": "host.get",
		                    "params": { "output":["hostid","status","host"]},
		                    "auth": self.authID,
		                    "id": 1})
		res = self.get_data(data)['result']
		#可以返回完整信息
		#return res
		hostsid = []
		if (res != 0) and (len(res) != 0):
			for host in res:
				if host['status'] == '1':
					hostsid.append({host['host']:host['hostid']})
				elif host['status'] == '0':
					hostsid.append({host['host']:host['hostid']})
				else:
					pass
		return hostsid

	#查找一台主机的所有图形和图形id
	def hostgraph_get(self, hostname):
		data = json.dumps({
		                    "jsonrpc": "2.0",
		                    "method": "host.get",
		                    "params": { "selectGraphs": ["graphid","name"],
		                                "filter": {"host": hostname}},
		                    "auth": self.authID,
		                    "id": 1})
		res = self.get_data(data)['result']
		#可以返回完整信息rs,含有hostid
		print res
		return res[0]['graphs']

	#获取历史数据,history必须赋值正确的类型0,1,2,3,4 float,string,log,integer,text
	def history_get(self, itemid, i):
		data = json.dumps({
                            "jsonrpc": "2.0",
                            "method": "history.get",
                            "params": { "output": "extend",
                                        "history": i,
                                        "itemids": itemid,
                                        "sortfield": "clock",
                                        "sortorder": "DESC",
                                        "limit": 10},
                            "auth": self.authID,
                            "id": 1})
		res = self.get_data(data)['result']
		return res

a = Zabbix()
print a.hostsid_get()
print a.hostgraph_get('Zabbix server')
print a.history_get('526',1)
