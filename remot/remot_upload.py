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
def upload_remote(remote_file_path, local_file_path, ip, port, user, passwd, mv, cmd):
	try:
		if mv:
			command(ip, port, user, passwd, mv)
		up = paramiko.Transport(ip, int(port))
		up.connect(username = user, password = passwd)
		sftp = paramiko.SFTPClient.from_transport(up)
		remote_path = remote_file_path   #远程目录及上传的文件名
		local_path = local_file_path #本地要上传的文件
		sftp.put(local_path, remote_path)
		up.close()
		print("%s Upload Ok\n" % ip)
		if cmd:
			command(ip, port, user, passwd, cmd)
	except:
		print("%s Upload Error\n" % ip)

######################################
#   这个函数是负责远程执行shell命令
######################################
def command(ip, port, username, passwd, cmd):
	try:
		com = paramiko.SSHClient()
		com.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		com.connect(ip, int(port), username, passwd, timeout=5)
		stdin, stdout, stderr = com.exec_command(cmd)
		filename_list = stdout.readlines()
		stdin.write("Y")
		com.close()
		print("%s\tCommand Executive OK\n" % ip)
	except:
		print("%s\tCommand Executive Error\n" % ip)


if __name__=="__main__":
	remote_path = '/usr/local/test.tar.gz'
	local_path = '/usr/local/test.tar.gz'
	cd_path = "cd /usr/local/ ;"
	tar = "tar -zxvf"
	file = "test.tar.gz"
	cmd = "%s %s %s" % (cd_path, tar, file)
	mv_ngx = "mv test test_bak ;"
	mv_ngx_gz = "mv test.tar.gz test.tar.gz.bak"
	mv = "%s %s %s" % (cd_path, mv_ngx, mv_ngx_gz)
	hosts = open("linux_server.list")
	threads = []   #使用线程
	for host in hosts:
		if host:
			ip, user, passwd, port = host.split(":")
			p = threading.Thread(target = upload_remote, args = (remote_path, local_path, ip, port, user, passwd, mv, cmd))
			p.start()











