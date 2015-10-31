#!/opt/python3/bin/python3
#coding:utf-8
#Author by 453604341@qq.com

#######################################
#   此文件为从远程机上下载文件至本地，
#######################################

import fileinput
import os
import re
import sys 
import string
import time
import paramiko
from subprocess import call

t = paramiko.Transport("ip", 22)
t.connect(username = "root", password = "123456")
sftp = paramiko.SFTPClient.from_transport(t)
remote_path = '/usr/local/text.txt'
local_path = '/usr/local/text.txt'
sftp.get(remote_path, local_path)
t.close()

