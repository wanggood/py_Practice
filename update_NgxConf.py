#!/opt/python3/bin/python3
#coding:utf-8
#Author by 453604341@qq.com

#######################################
#	此文件为批量更新nginx部分配置，
#######################################

import fileinput
import os
import re
import sys
import string
import time
from subprocess import call

s_all = """
	location ~* ^(.*)\/\.svn\/ {
			deny all;
		}
	location ~* \.(tar|gz|zip|tgz|sh)$ {
			deny all;
		}
"""

s_svn = """
	location ~* ^(.*)\/\.svn\/ {
			deny all;
		}
"""

s_tar = """
	location ~* \.(tar|gz|zip|tgz|sh)$ {
			deny all;
		}
"""

def ffile_insert(fname, str):
	r = '}'
	f = open(fname)
	old = f.read()
	num = int(re.search(r, old).start()) #正则匹配记录起始位置
	f_input = fileinput.input(fname, inplace=1)
	for line in f_input:
		if r in line:
			print(line.rstrip())
			print("\n"+str+"\n")
			f.seek(num+2)
			print(f.read())
			break
		else:
			print(line.rstrip())
	f.close()
	f_input.close()
	#print("配置文件 %s 已经添加成功！" % fname)

#######################################
# 这个函数是往配置文件中添加需要的配置----
# 先从文件开头记录到location段的长度lengthA，然后seek到---
# lengthA，再重新获取新的内容，再记录用for到location的最后字符}
# 插入内容时，seek到这两段长度和，再read后半部分配置，
# 然后再seek到两段长度和，再write该配置项，
# 最后write后半部分配置
##########################################
def file_insert(fname, str):
	loca = 'location'
	r = '}'
	lengthB = 0
	f = open(fname)
	old = f.read()
	lengthA = int(re.search(loca, old).start())
	f.seek(lengthA, 0)
	old = f.read()
	f.close()
	for li in old:
		lengthB += 1
		if r == li:
			break
	f = open(fname, "r+")
	f.tell()
	sum_length = lengthA + lengthB
	f.seek(sum_length, 0)
	back_content = f.read() #读取后半部分的配置
	f.seek(sum_length, 0)   #seek到插入的位置
	f.write("\n"+str+"\n")
	f.write(back_content)
	f.close()


##########################################
#  这个函数是遍历各个配置文件是否有该配置项----
#  有则忽略，没有则调用file_insert函数添加
#########################################
def file_list(f_dir):
	rsvn = '\.svn'
	rtar = '\(tar\|gz\|zip\|tgz\|sh\)'
	if os.path.exists(f_dir): #判断路径是否存在
		for f_name in os.listdir(f_dir): #遍历整个文件夹
			f_path = os.path.join(f_dir, f_name)#把目录和文件名合成一个路径
			f1 = open(f_path)
			f1_old = f1.read()
			f1.close()
			if re.findall(rsvn, f1_old) and re.findall(rtar, f1_old):
				print("%s 已经加过相关配置，忽略配置文件" % f_path)
				continue
			elif re.findall(rsvn, f1_old):
				file_insert(f_path, s_tar)
			elif re.findall(rtar, f1_old):
				file_insert(f_path, s_svn)
			else:
				file_insert(f_path, s_all)
	else:
		print("%s 该路径不存在! " % f_dir)


##########################################
#  这个函数是把原有的配置备份----
##########################################
def file_backup(f_dir):
	bak_dir = "/usr/local/my_python/my_word/nginx_config_bak/" + time.strftime('%Y_%m_%d_%H_%M')
	if not os.path.exists(bak_dir):
		os.makedirs(bak_dir) #新建该目录
		if os.path.exists(f_dir):
			cp = "cp -rp"
			cmd = "%s %s %s" % (cp, f_dir, bak_dir)
			call(cmd, shell=True)

if __name__ == "__main__":
	f_dir = "/usr/local/my_python/my_word/vhosts"
	file_backup(f_dir)
	file_list(f_dir)
	print("-"*30,"\n所有nginx配置文件更新完成!\n")

