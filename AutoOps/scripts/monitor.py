import time
import MySQLdb as mysql
import os

db = mysql.connect(user="root",passwd="123456",db="AutoOps",host="localhost")
db.autocommit(True)
cur = db.cursor()

def getMem():
    with open('/proc/meminfo') as f:
        total = int(f.readline().split()[1])
        free = int(f.readline().split()[1])
        buffers = int(f.readline().split()[1])
        cache = int(f.readline().split()[1])
    mem_use = total-free-buffers-cache
    t = int(time.time())
    sql = 'insert into monitor_mem (mem_values,mem_times) value (%s,%s)'%(mem_use/1024,t)
    cur.execute(sql)
    print mem_use/1024
def load_stat():  
    loadavg = {}  
    f = open("/proc/loadavg")  
    con = f.read().split()  
    f.close() 
    loadavg['lavg_1']=con[0]  
    loadavg['lavg_5']=con[1]  
    loadavg['lavg_15']=con[2]  
    loadavg['nr']=con[3]  
    loadavg['last_pid']=con[4]
    type = ['lavg_1','lavg_5','lavg_15']
    t = int(time.time())
    li = []
    for i in type:
        tmp_list = [i,loadavg[i],t]
        li.append(tmp_list)
    sql = 'insert into monitor_cpu_load_info (cpu_type,cpu_loads_val,info_times) value (%s,%s,%s)'
    cur.executemany(sql,li)
    print li 

def net_stat():  
    net = []  
    f = open("/proc/net/dev")  
    lines = f.readlines()  
    f.close()  
    for line in lines[2:]:  
        con = line.split()  
        intf = dict(  
            zip(  
                ( 'interface','ReceiveBytes','ReceivePackets',  
                  'ReceiveErrs','ReceiveDrop','ReceiveFifo',  
                  'ReceiveFrames','ReceiveCompressed','ReceiveMulticast',  
                  'TransmitBytes','TransmitPackets','TransmitErrs',  
                  'TransmitDrop', 'TransmitFifo','TransmitColls',  
                  'TransmitCarrier','TransmitCompressed' ),  
                ( con[0].rstrip(':').split(':')[0],con[0].rstrip(':').split(':')[1],int(con[1]),int(con[2]),  
                  int(con[3]),int(con[4]),int(con[5]),  
                  int(con[6]),int(con[7]),int(con[8]),  
                  int(con[9]),int(con[10]),int(con[11]),  
                  int(con[12]),int(con[13]),int(con[14]),  
                  int(con[15]), )  
            )  
        )  
  
        net.append(intf)  
    print net  

def disk_stat():  
    hd={}  
    disk = os.statvfs("/")  
    hd['available'] = disk.f_bsize * disk.f_bavail  
    hd['capacity'] = disk.f_bsize * disk.f_blocks  
    hd['used'] = disk.f_bsize * disk.f_bfree  
    print hd
	
while True:
    time.sleep(300)
    getMem()
    load_stat()
    #net_stat()
    #disk_stat()
