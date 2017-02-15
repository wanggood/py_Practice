#!/opt/python3/bin/python3

#这里email_password文件为发件者邮箱密码

import smtplib
import os
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender = 'jin100jg@sina.com'       #发件者邮箱
mailto_list = ['453604341@qq.com'] #接收者邮箱
mail_host = 'smtp.sina.com'        #smtp服务器

def send_mail(sender, mail_pass, to_receivers, msg):
	try:
		s = smtplib.SMTP()
		s.connect(mail_host) #连接smtp服务器
		s.login(sender, mail_pass) #登录
		s.sendmail(sender, to_receivers, msg.as_string()) #发送
		s.quit()
		return True
	except Exception:
		return False

if __name__=='__main__':
	passwd_path = './email_password'
	if os.path.isfile(passwd_path):
		p = open(passwd_path)
		for i in p:
			mail_pass = i.split("\n") #以换行为分隔，
			mail_pass = ''.join(mail_pass) #将列表转为字符串
	else:
		print("open email_password Error!")
		sys.exit()

#----------这是一个带html格式的邮件-------
	theme = "jingang" + "<" + sender + ">"
	content = "<p>点这里：</p><a href='http://www.xingyum8023.com'>礼物在我的主页里</a>"
	msg = MIMEText(content, _subtype='html', _charset='gb2312')
	msg['Subject'] = 'This is a gift for you' #设置邮件主题
	msg['From'] = theme #设置邮件头:发件人
	msg['To'] = ";".join(mailto_list) #收件人
	
#-----下面发送一个带附件的邮件--------
	attach1 = MIMEText(open("test.txt",'rb').read(), 'base64', 'utf-8')
	attach1["Content-Type"] = 'application/octet-stream'
	attach1["Content-Disposition"] = 'attachment; filename = "test.txt"'
	attach1['Subject'] = 'This is a test word'
	attach1['From'] = theme
	attach1['To'] = ";".join(mailto_list)

	if send_mail(sender, str(mail_pass), mailto_list, attach1):
		print("发送ok")
	else:
		print("发送错误")

