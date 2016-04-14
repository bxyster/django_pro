#!/usr/bin/env python
#coding:utf8
import global_settings
import MySQLdb
from AutoOps import settings
import Queue
import threading
import time
import sys,os


#数据库操作
class mydb():
	def __init__(self,host,user,passwd,db,port):
		self.host = host
		self.user = user
		self.passwd = passwd
		self.db = db
		self.port = port
		try:
			self.conn = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,port=self.port)
			self.conn.select_db(self.db)
			self.cur = self.conn.cursor()
		except MySQLdb.Error,e:
			print 'mysql error msg: ',e
	#执行语句
	def dbexec(self,dbcmd):
		self.cur.execute(dbcmd)
		self.result = self.cur.fetchall()
		self.conn.commit()
		return self.result
	#关闭链接
	def dbclose(self):
		self.cur.close()
		self.conn.close()

#线程操作
class myThread (threading.Thread):
	def __init__(self, threadID, name, q):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.q = q
	def run(self):
		#print "Starting " + self.name
		process_data(self.name, self.q)
		#print "Exiting " + self.name

def process_data(threadName, q):
	while not exitFlag:      # 死循环等待
		if not q.empty():    # 判断队列是否为空
			data = q.get()
			data = data.split(':')
			if data[2] == '2':
				print "python %s" % (data[1])
				task_result = "python %s" % (data[1])
			elif data[2] == '1':
				print "python %s %s" % (data[0],data[1])
				task_result = "python %s %s" % (data[0],data[1])
			print data[0],data[1],task_result,'1',data[3]
			write_db(data[0],data[1],task_result,'1',data[3])
#		time.sleep(1)

def update_db(status_id,task_level,times,task_id):
	queueLock.acquire()
	try:
		db.dbexec('UPDATE cmdb_taskmanage set cron_status = %s ,cron_result = %s,cron_total_time = %s where id=%s'% 
		(status_id,task_level,times,task_id))
	except:
		pass
	queueLock.release()
	
def write_db(ips,cmds,results,status,ids):
	queueLock.acquire()
	try:
		db.dbexec('INSERT into cmdb_taskdetail(ip,task_cmds,task_result,task_status,task_id_id) VALUES ("%s","%s","%s","%s","%s")' % (ips,cmds,results,status,ids))
	except:
		pass
	queueLock.release()

if __name__ == '__main__':
	#定义退出标签
	exitFlag = 0
	start_time = int(time.time())
	db = mydb(settings.DATABASES['default']['HOST'],
		settings.DATABASES['default']['USER'],
		settings.DATABASES['default']['PASSWORD'],
		settings.DATABASES['default']['NAME'],
		settings.DATABASES['default']['PORT'])
	result = db.dbexec('select a.id,ip,cron_content,cron_type from cmdb_taskmanage as a,cmdb_ipmanage as b where a.group_name_id = b.group_name_id and  cron_status != 0 and cron_start_time <= NOW()')
	#处理查询数据
	a_list = []
	b_list = []
	for m in result:
		a_list.append(int(m[0]))
		b_list.append("%s:%s:%s:%s"% (m[1],m[2],m[3],m[0]))
	a_list = set(a_list)
	print a_list,b_list
			
	#定义线程数
	threadNum = 5
	#定义锁方法,防止同时修改数据库
	queueLock = threading.Lock()     
	#定义队列,队列与锁并无关联
	workQueue = Queue.Queue(10)
	threads = []
	threadID = 1
	#批量开始修改任务状态
	for task_id in a_list:
		times = 0
		status_id = 1
		task_level = 1
		update_db(status_id,task_level,times,task_id)
	
	for tName in xrange(threadNum):
		thread = myThread(threadID, tName, workQueue)
		thread.start()
		threads.append(thread)
		threadID += 1
	
	for word in b_list:
		workQueue.put(word)
	
	while not workQueue.empty():   # 死循环判断队列被处理完毕
		pass
	
	exitFlag = 1
	
	for t in threads:
		t.join()
	
	#print "Exiting Main Thread"
	#本次任务结束修改任务状态
	total_time = int(time.time()) - start_time
	print total_time
	for task_id in a_list:
		times = total_time
		status_id = 0
		task_level = 2
		update_db(status_id,task_level,times,task_id)
