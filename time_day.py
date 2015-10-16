#!/opt/python3/bin/python3

################################
#这个文件是根据给定的年份和周，算出那一周的第一天日期
#和最后一天日期。
#
#思路：先算出那一年的第一天日期和星期天的日期，然后周*7，
#多少天就加多少天得天最后一天日期，再减去6天就得到该周的第一天
###############################

import time
import datetime
import calendar

def day_time(year, month):
	year = int(year)
	month = int(month)
	week_list = (calendar.monthcalendar(year, 1))[0]
	for i in range(0, 7):
		if str(week_list[i]) != "0":
			day_ = week_list[i]
			break
	day_start = str(year) + "-" + "01" + "-" + ("0" + str(day_))
	day_start = day_start + " " + "23:30:30"
	timearray = time.strptime(day_start, "%Y-%m-%d %H:%M:%S")
	timestamp = int(time.mktime(timearray))
	dateArray = datetime.datetime.utcfromtimestamp(timestamp)
	datelast = dateArray + datetime.timedelta(days=6-i)
	if month == 1:
		print(month,"周的第一天日期:",dateArray)
		print(month,"周的最后一天日期:",datelast)
	if month > 1 and month < 53:
		day_month = (month * 7)-7
		datelast = datelast + datetime.timedelta(days=day_month)
		dateArray = datelast - datetime.timedelta(days=6)
		print(month,"周的第一天日期:",dateArray)
		print(month,"周的最后一天日期:",datelast)
	else:
		print("没有这个周哦")

if __name__ == "__main__":
	try:
		year = input("请输入哪一年:")
		week = input("请输入第几周:")
	except:
		print("请正确输入年份!")
	day_time(year, week)


