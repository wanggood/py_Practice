#!/opt/python3/bin/python3
import pymysql
import os

Establish_table = """create table jin (
	id int(5) auto_increment not null primary key,
	name char(15) collate utf8_bin not null,
	address varchar(50) collate utf8_bin,
	year date);
	"""

sqlfile_upload_log = """create table sqlfile_upload_log (
    ip varchar(16) not null primary key,
	tar_name varchar(50) collate utf8_bin not null,
	md5 varchar(50) not null,
	flag int(2) not null,
	error_log varchar(100) collate utf8_bin not null,
	uptime datetime);
	"""
passwd_path = "passwd.txt"
if os.path.isfile(passwd_path):
	hosts = open(passwd_path)
	ip, passwd, user, port = hosts.readline().split(":")

class py_mysql:

	def __init__(self,mysql_command):
		self.mysql_command = mysql_command

	def SignIn(self):
		db = pymysql.connect(host=ip,user=user,password=passwd,db='wang',port=int(port),charset='utf8mb4')
		cursor = db.cursor() #获取操作游标
		cursor.execute(self.mysql_command)
        results = cursor.fetchall() #获取所有记录列表
		#for row in results:
		#	print(row)
		#print(results[1][0])
		#print(results[2][0])
		print(results[0][3])
		
		
		#for row in results:
		#	id = row[0]
		#	name = row[1]
		#	address = row[2]
		#	time = row[3]
		#	score = row[4]
		#	print(id, name, address, time, score)
		#db.commit() #提交到数据库，查询时可以不用
		cursor.close()
		db.close()
		#print("Singn in table ok!")
	#def Establish()

if __name__=="__main__":
	sq1 = """insert into jin values('','张三','深圳','1995-9-10');
			insert into jin values('','李四','广州','1994-7-26');
			insert into jin values('','王小二','北京','1993-12-25');
			insert into jin values('','小曦','上海','1996-8-19');
		"""
	sq2 = """select * from jin where year between '1995-01-01' and '1999-01-01';
		"""
	sq3 = """alter table jin add column age int(3) not null default 0 after name;
	"""
	sq4 = """alter table jin drop column age;"""
	sq5 = """select yuwu from jin;"""
	s = py_mysql(sq2)
	s.SignIn()
	
