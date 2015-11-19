#!/opt/python3/bin/python3
#coding:utf-8
#Author by 453604341@qq.com

#######################################
#   此文件为上传文件至多台远程机并解压，
#	另外一个文件每行格式：ip:user:passwd:port
#######################################

import fileinput
import os
import re
import sys 
import string
import time
import paramiko
import threading
from subprocess import call

class up_remote:
	com = 0
	def __init__(self, remote_file_path, local_file_path, f_size, ip, port, user, passwd):
		self.remote_file_path = remote_file_path
		self.local_file_path = local_file_path
		self.f_size = f_size
		self.ip = ip
		self.port = port
		self.user = user
		self.passwd = passwd

	def upload_remote(self, bak_mkdir, cmd):
		if bak_mkdir:
			self.command(bak_mkdir)
		try:
			up = paramiko.Transport(self.ip, int(self.port))
			up.connect(username = self.user, password = self.passwd)
			sftp = paramiko.SFTPClient.from_transport(up)
			sftp.put(self.local_file_path, self.remote_file_path)
			up.close()
			print("%s Upload Ok,\n" % self.ip)
		except:
			print("%s Upload Error\n" % self.ip)
			self.Error_log(self.ip, [], "upload error")
		com, file_size = self.command(['ls -al ' + self.remote_file_path])
		com.close()
		if int(file_size) == int(self.f_size):
			self.command(cmd)
		else:
			print("%s Upload file size error\n" % self.ip)
			self.Error_log(self.ip, [], "file size error")

	######################################
	#   这个函数是负责远程执行shell命令
	######################################
	def command(self, cmd):
		try:
			com = paramiko.SSHClient()
			com.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			com.connect(self.ip, int(self.port), self.user, self.passwd, timeout=5)
			for cmd_ in cmd:
				stdin, stdout, stderr = com.exec_command(cmd_)
				stdin.write("Y")
				file_list = stdout.readlines()
				if re.findall(r"ls", cmd_):
					if re.findall(r"ls", cmd_)[0] == "ls":
						file_size = (" ".join(file_list)).split(" ")[4]
						return com, file_size
			com.close()
			print("%s\tCommand Executive OK\n" % self.ip)
		except:
			print("%s\t %s Command Error\n" % self.ip, cmd)
			self.Error_log(self.ip, cmd, "command error")
	
	def Error_log(self, ip, command, reason):
		error_file = './error.log'
		com = " ".join(command)
		time_ = time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
		log_ = ("%s %s %s" % (ip, com, reason)) + "\n\n"
		f = open(error_file, 'a+')
		f.write(time_)
		f.write(log_)
		f.close()

if __name__=="__main__":
	remote_path = '/zywa/nginx.tar.gz'
	local_path = 'nginx.tar.gz'
	f_size = os.path.getsize(local_path)
	cmd = ['cd /zywa/ ; \
			tar -zxvf nginx.tar.gz ; ',
			'groupadd -r nginx ; \
			useradd -s /sbin/lologin -g nginx -r nginx ;',
			'mkdir /data ;',
			'mv /zywa/libluajit-5.1.so.2 /usr/lib64/ ;',
			'/zywa/nginx/sbin/nginx ;'
		  ]
	bak_mkdir = ['mkdir /zywa ; \
		  cd /zywa/ ; mv nginx nginx_bak ; \
		  mv nginx.tar.gz nginx.tar.gz.bak ; '
		 ]
	
	hosts = open("linux_server.list")
	threads = []   #使用线程池
	for host in hosts:
		if host:
			ip, user, passwd, port = host.split(":")
			up = up_remote(remote_path, local_path, f_size, ip, port, user, passwd)
			threads.append(threading.Thread(target = up.upload_remote, args = (bak_mkdir, cmd)))
			
	for t in threads:
		t.setDaemon(True)
		t.start() #启动所有线程
	for t in threads:
		t.join() #主(父)线程中等待所有子线程退出
	hosts.close()
