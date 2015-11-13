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

#######################################
#  这个函数是上传文件
#######################################
def upload_remote(remote_file_path, local_file_path, ip, port, user, passwd, mkdir_catalog, mv, cmd):
	if mv:
		command(ip, port, user, passwd, mv)
	if mkdir_catalog:
		command(ip, port, user, passwd, mkdir_catalog)
	try:
		up = paramiko.Transport(ip, int(port))
		up.connect(username = user, password = passwd)
		sftp = paramiko.SFTPClient.from_transport(up)
		remote_path = remote_file_path   #远程目录及上传的文件名
		local_path = local_file_path #本地要上传的文件
		sftp.put(local_path, remote_path)
		up.close()
		print("%s Upload Ok,\n" % ip)
	except:
		print("%s Upload Error\n" % ip)
		Error_log(ip, [], "upload error")
	if cmd:
		command(ip, port, user, passwd, cmd)

######################################
#   这个函数是负责远程执行shell命令
######################################
def command(ip, port, username, passwd, cmd):
	try:
		com = paramiko.SSHClient()
		com.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		com.connect(ip, int(port), username, passwd, timeout=5)
		for cmd_ in cmd:
			stdin, stdout, stderr = com.exec_command(cmd_)
			stdin.write("Y")
			filename_list = stdout.readlines()
		com.close()
		print("%s\tCommand Executive OK\n" % ip)
	except:
		print("%s\t %s Command Error\n" % ip, cmd)
		Error_log(ip, cmd, "command error")

def Error_log(ip, command, reason):
	error_file = './error.log'
	com = " ".join(command)
	time_ = time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
	log_ = ("%s %s %s" % (ip, com, reason)) + "\n\n"
	f = open(error_file, 'a+')
	f.write(time_)
	f.write(log_)
	f.close()

if __name__=="__main__":
	remote_path = '/zywa/test.tar.gz'
	local_path = '/usr/local/test.tar.gz'
	mkdir_catalog = ['cd / ; mkdir zywa']
	cmd = ['cd /zywa/ ; \
			tar -zxvf test.tar.gz ;'
		  ]
	mv = ['cd /zywa/ ; mv test test_bak ; \
		  mv test.tar.gz test.tar.gz.bak ;'
		 ]
	
	hosts = open("linux_server.list")
	threads = []   #使用线程
	for host in hosts:
		if host:
			ip, user, passwd, port = host.split(":")
			threads.append(threading.Thread(target = upload_remote, args = (remote_path, local_path, ip, port, user, passwd, mkdir_catalog, mv, cmd)))
			
	for t in threads:
		t.setDaemon(True)
		t.start() #启动所有线程
	for t in threads:
		t.join() #主(父)线程中等待所有子线程退出

