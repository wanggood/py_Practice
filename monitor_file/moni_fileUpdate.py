#!/opt/python3/bin/python3

import paramiko, os, sys, datetime, time, pymysql
from pyinotify import WatchManager, Notifier, ProcessEvent,IN_DELETE, IN_CREATE, IN_MODIFY

#----表的结构----
"""create table sqlfile_upload_log (
	ip varchar(16) not null primary key,   #机器ip
    tar_name varchar(50) collate utf8_bin not null, #备份文件名字
	md5 varchar(50) not null,  #备份文件md5
	flag int(2) not null,      #0成功，1失败
	error_log varchar(100) collate utf8_bin not null, #错误日志
	uptime datetime);    #更新时间
"""

#----获取账号密码----
passwd_path = "passwd.txt"
if os.path.isfile(passwd_path):
	hosts = open(passwd_path)
	sshbak_ip, passwd1, user1, port1 = hosts.readline().split(":")
	sql_ip, passwd2, user2, port2 = hosts.readline().split(":")
	hosts.close()

#--需要备份的数据库路径--
find_path = '/usr/local/my_python'

def log2db(ip, tar_name, md5, flag, error='0'):
	try:
		tar_name = os.path.split(tar_name)[1]
		now = time.strftime("%Y-%m-%d %H:%M:%S") #当前时间
		conn = pymysql.connect(host=sql_ip, user=user2, password=passwd2, db='wang', port=int(port2), charset='utf8mb4')
		cursor = conn.cursor()
		sql = "select ip from sqlfile_upload_log where ip='%s';" % ip
		cursor.execute(sql)     #查找库中是否有记录
		res = cursor.fetchall() #获取所有记录列表
		if len(res) == 0:
			inster_sql = "insert into sqlfile_upload_log values('%s','%s','%s','%s','%s','%s');" % (ip,tar_name,md5,flag,error,now)
			cursor.execute(inster_sql) #初始日志写入
			conn.commit() #提交到库
		else:
			update_sql = "update sqlfile_upload_log set md5='%s', flag='%s', error_log='%s', uptime='%s' where ip='%s';" % (md5,flag,error,now,ip)
			cursor.execute(update_sql) #更新mysql中的日志
			conn.commit()
		cursor.close()
		conn.close()
	except Exception:
		print("log mysql error")

#-------获取本地ip-----------
def find_ip():
	ip = os.popen("/sbin/ip a|grep 'global eth0'").readlines()[0].split()[1].split('/')[0]
	if "172.110." in ip:
		ip = os.popen("/sbin/ip a|grep 'global eth1'").readlines()[0].split()[1].split("/")[0]
	return ip

#-----执行本地的md5命令-----
def md5sum(file_name):
	if os.path.isfile(file_name):
		f =open(file_name, 'rb')
		py_ver = sys.version[:3] #获取python版本
		if py_ver == "2.4":
			import md5 as hashlib
		else:
			import hashlib
			md5 = hashlib.md5(f.read()).hexdigest()
			f.close()
			return md5
	else:
		return 0

#------执行远程备份机的md5命令----
def remote_md5(file_name):
	try:
		s = paramiko.SSHClient()
		s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		s.connect(hostname=sshbak_ip, port=int(port1), username=user1, password=passwd1)
		conm = "/usr/bin/md5sum %s" % (file_name)
		stdin, stdout, stderr = s.exec_command(conm)
		result = stdout.readlines()[0].split()[0].strip()
		s.close()
		return result
	except Exception:
		print("remote_md5 Error")
		return 0

#----开始远程备份------
def back_file(ip, tar_name, tar_md5):
	remote_dir = '/data/sql' #备份的位置
	file_name = os.path.join(remote_dir, os.path.split(tar_name)[1])
	try:
		t = paramiko.Transport(sshbak_ip, int(port1))
		t.connect(username=user1, password=passwd1)
		sftp = paramiko.SFTPClient.from_transport(t)
		sftp.put(tar_name, file_name)
		t.close()
		os.remove(tar_name) #删除在本地打包的文件
		remot_md5 = remote_md5(file_name)
		if remot_md5 == tar_md5:
			log2db(ip, tar_name, tar_md5, 0)
		else:
			log2db(ip, tar_name, tar_md5, 1, 'remot_md5!=tar_md5')
	except Exception:
		print("back connect error")
		log2db(ip, tar_name, tar_md5, 1, "back connect error")
		if os.path.isfile(tar_name):
			os.remove(tar_name)

def back_sql():
	ip = find_ip()
	tar_name = "%s.tar.gz" % ip  #打包后的文件名
	sql_conn = "/usr/bin/find %s -type f -name '*.sql'|/usr/bin/xargs /bin/tar zcvPf %s" % (find_path, tar_name)
	sql_tar = os.popen(sql_conn).readlines() #压缩本地sql文件
	tar_md5 = md5sum(tar_name)
	if tar_md5 != 0:
		back_file(ip, tar_name, tar_md5)
	else:
		error_log = "%s not find" % tar_name
		log2db(ip, tar_name, tar_md5, 1, error_log)

class PFilePath(ProcessEvent):
	def process_IN_CREATE(self, event):
		if os.path.splitext(event.name)[1] == ".sql":
			text = "Create file: %s" % os.path.join(event.path, event.name)
			#print(text)
			back_sql()

	def process_IN_MODIFY(self, event):
		if os.path.splitext(event.name)[1] == ".sql":
			text = "Modify file: %s" % os.path.join(event.path, event.name)
			#print(text)
			back_sql()

#------------主监控函数-----------
def FSMonitor():
	back_sql()
	"""
	wm = WatchManager()
	mask = IN_CREATE | IN_MODIFY
	notifier = Notifier(wm, PFilePath())
	wdd = wm.add_watch(GM_path, mask, rec=True)
	print("now starting monitor %s" % GM_path)
	while True:
		try:
			notifier.process_events()
			if notifier.check_events():
				notifier.read_events()
		except KeyboardInterrupt:
			notifier.stop()
			break
"""
if __name__=="__main__":
	FSMonitor()



