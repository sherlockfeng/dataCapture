#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests
import sys,os
from bs4 import BeautifulSoup
import ConfigParser,traceback
from util import Utils
from printLog import Logger
import threading
import re
import random
import time
from dbPool import Mysql
from headerConfig import Headers
reload(sys)
sys.setdefaultencoding('utf-8')

class ipProxy():
  	
	user_agents = []
	headers = {}
	utils = Utils()

	def __init__(self):
		self.Loggers = Logger('ipProxy')
		self.user_agents = Headers().user_agents
		self.headers = Headers().headers
		self.cfg = self.utils.pathToConfig()
		self.mysql = Mysql(self.cfg.get('DB', 'DBHOST'), int(self.cfg.get('DB', 'DBPORT')), self.cfg.get('DB', 'DBUSER'), self.cfg.get('DB', 'DBPWD'), 3, 5)
	
	def get_ip_from_xici(self):
		Loggers = Logger(special_log_file = 'getProxyXiCi')
		while 1 == 1:
			try:
				avalibleIpsOneWeb = []
				startGetIpTime = time.time()
				startGetIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
				title = u'西祠代理'
				Loggers.Info('>>>>> ' + startGetIpTimeFormat + '|' + title + u'|开始抓取ip <<<<<')
				url = 'http://www.xicidaili.com/nn/'
				head = self.headers
				head['user-agent'] = random.choice(self.user_agents)
				try:
					Loggers.Info('>>>>> ' + title + u'|开始请求url ' + url + ' <<<<<')
					r = requests.get(url, timeout=10, headers=head)
					soup = BeautifulSoup(r.text, "html.parser")
					list = soup.find('table', attrs={'id': 'ip_list'}).find_all('td')
					strText = ''
					ips = []
					for l in list:
						content = l.get_text().strip()
						if re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', content):
							strText = content
						if re.match(r'^([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{4}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$', content):
							strText = strText + ':' + content
							ips.append(strText)
					endGetIpTime = time.time()
					endGetIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
					Loggers.Info('>>>>> ' + endGetIpTimeFormat + '|' + title + u'|结束抓取ip,共抓取' + str(len(ips)) + '条 <<<<<')
					Loggers.Info('>>>>> ' + endGetIpTimeFormat + '|' + title + u'|开始检查ip是否可用,抓取共耗时' + str(endGetIpTime - startGetIpTime) + ' <<<<<')

					for ip in ips:
						Loggers.Info(u'>>>>> 开始检查ip:' + str(ip) + ' <<<<<')
						start = time.time()
						if self.utils.checkIpForAJK(ip):
							end = time.time()
							avalibleIpsOneWeb.append({
								'source': 'xici',
								'ip': ip,
								'time':str(end - start)
							})
							Loggers.Info('>>>>> ip:' + str(ip) + u' 可用<<<<<')
						else:
							Loggers.Info('>>>>> ip:' + str(ip) + u' 不可用<<<<<')
					endCheckIpTime = time.time()
					endCheckIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
					Loggers.Info('>>>>> ' + endCheckIpTimeFormat + '|' + title + u'|结束检查ip是否可用,检查共耗时' + str(endCheckIpTime - endGetIpTime) + ' <<<<<')
					Loggers.Info('>>>>> ' + title + u'|成功率:' + str(len(avalibleIpsOneWeb)) + '-' +str(len(ips)) + ' <<<<<')
					Loggers.Info('>>>>> ' + endCheckIpTimeFormat + '|' + title + u'|结束,抓取到' + str(len(avalibleIpsOneWeb)) + u'条可用ip,共耗时' + str(endCheckIpTime - startGetIpTime) + ' <<<<<')
					# self.avalibleIps.append(avalibleIpsOneWeb)
					self.insert_data(Loggers, avalibleIpsOneWeb)
				except BaseException, e:
					Loggers.Error(u'>>>>> 请求url出错 ' + str(e) + '<<<<<')
			except BaseException, e:
				Loggers.Error(u'>>>>> 抓取ip循环出错 ' + str(e) + '<<<<<')
			time.sleep(10)
	
	def get_ip_from_ip3366(self):
		Loggers = Logger(special_log_file = 'getProxyIp336')
		while 1 ==1:
			try:
				avalibleIpsOneWeb = []
				startGetIpTime = time.time()
				startGetIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
				title = u'云代理'
				Loggers.Info('>>>>> ' + startGetIpTimeFormat + '|' + title + u'|开始抓取ip <<<<<')
				url = ['http://www.ip3366.net/free/','http://www.ip3366.net/free/?stype=1&page=2']
				# url = ['http://www.ip3366.net/free/']
				head = self.headers
				head['user-agent'] = random.choice(self.user_agents)
				ips = []
				for u in url:
					try:
						Loggers.Info('>>>>> ' + title + u'|开始请求url ' + u + ' <<<<<')
						r = requests.get(u, timeout = 10, headers=head)
						soup = BeautifulSoup(r.text, "html.parser")
						list = soup.find('div', attrs={'id': 'list'}).find_all('td')
						strText = ''
						for l in list:
							content = l.get_text().strip()
							if re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', content):
								strText = content
							if re.match(r'^([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{4}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$', content):
								strText = strText + ':' + content
								ips.append(strText)
					except BaseException, e:
						Loggers.Error(u'>>>>> 请求url出错 ' + str(e) + '<<<<<')
				endGetIpTime = time.time()
				endGetIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
				Loggers.Info('>>>>> ' + endGetIpTimeFormat + '|' + title + u'|结束抓取ip,共抓取' + str(len(ips)) + '条 <<<<<')
				Loggers.Info('>>>>> ' + endGetIpTimeFormat + '|' + title + u'|开始检查ip是否可用,抓取共耗时' + str(endGetIpTime - startGetIpTime) + ' <<<<<')

				for ip in ips:
					start = time.time()
					Loggers.Info(u'>>>>> 开始检查ip:' + str(ip) + ' <<<<<')
					if self.utils.checkIpForAJK(ip):
						end = time.time()
						Loggers.Info('>>>>> ip:' + str(ip) + u' 可用<<<<<')
						avalibleIpsOneWeb.append({
							'source': 'IP366',
							'ip': ip,
							'time':str(end - start)
						})
					else:
						Loggers.Info('>>>>> ip:' + str(ip) + u' 不可用<<<<<')
				endCheckIpTime = time.time()
				endCheckIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
				Loggers.Info('>>>>> ' + endCheckIpTimeFormat + '|' + title + u'|结束检查ip是否可用,检查共耗时' + str(endCheckIpTime - endGetIpTime) + ' <<<<<')
				Loggers.Info('>>>>> ' + title + u'|成功率:' + str(len(avalibleIpsOneWeb)) + '-' +str(len(ips)) + ' <<<<<')
				Loggers.Info('>>>>> ' + endCheckIpTimeFormat + '|' + title + u'|结束,抓取到' + str(len(avalibleIpsOneWeb)) + u'条可用ip,共耗时' + str(endCheckIpTime - startGetIpTime) + ' <<<<<')
				# self.avalibleIps.append(avalibleIpsOneWeb)
				self.insert_data(Loggers, avalibleIpsOneWeb)
			except BaseException, e:
				Loggers.Error(u'>>>>> 抓取ip循环出错 ' + str(e) + '<<<<<')
			time.sleep(10)

	def get_ip_from_66ip(self):
		Loggers = Logger(special_log_file = 'getProxy66Ip')
		while 1 == 1:
			try:
				avalibleIpsOneWeb = []
				startGetIpTime = time.time()
				title = u'安小莫'
				startGetIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
				Loggers.Info('>>>>> ' + startGetIpTimeFormat + '|' + title + u'|开始抓取ip <<<<<')
				url = 'http://www.66ip.cn/mo.php?sxb=&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=http%3A%2F%2Fwww.66ip.cn%2F%3Fsxb%3D%26tqsl%3D100%26ports%255B%255D2%3D%26ktip%3D%26sxa%3D%26radio%3Dradio%26submit%3D%25CC%25E1%2B%2B%25C8%25A1'
				head = self.headers
				head['user-agent'] = random.choice(self.user_agents)
				iplist = []
				try:
					Loggers.Info('>>>>> ' + title + u'|开始请求url ' + url + ' <<<<<')
					r = requests.get(url, timeout = 10, headers=head)
					r.encoding = 'gb2312'
					p = r'(?:((?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5]))\D+?(6[0-5]{2}[0-3][0-5]|[1-5]\d{4}|[1-9]\d{1,3}|[0-9]))'
					iplist = re.findall(p,r.text)
					ips = []
					for item in iplist:
						ips.append(item[0] + ':' + item[1])
					endGetIpTime = time.time()
					endGetIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
					Loggers.Info('>>>>> ' + endGetIpTimeFormat + '|' + title + u'|结束抓取ip,共抓取' + str(len(ips)) + '条 <<<<<')
					Loggers.Info('>>>>> ' + endGetIpTimeFormat + '|' + title + u'|开始检查ip是否可用,抓取共耗时' + str(endGetIpTime - startGetIpTime) + ' <<<<<')
					for ip in ips:
						start = time.time()
						Loggers.Info(u'>>>>> 开始检查ip:' + str(ip) + ' <<<<<')
						if self.utils.checkIpForAJK(ip):
							end = time.time()
							avalibleIpsOneWeb.append({
								'source': '66ip',
								'ip': ip,
								'time':str(end - start)
							})
							Loggers.Info('>>>>> ip:' + str(ip) + u' 可用<<<<<')
						else:
							Loggers.Info('>>>>> ip:' + str(ip) + u' 不可用<<<<<')
					endCheckIpTime = time.time()
					endCheckIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
					Loggers.Info('>>>>> ' + endCheckIpTimeFormat + '|' + title + u'|结束检查ip是否可用,检查共耗时' + str(endCheckIpTime - endGetIpTime) + ' <<<<<')
					Loggers.Info('>>>>> ' + title + u'|成功率:' + str(len(avalibleIpsOneWeb)) + '-' +str(len(ips)) + ' <<<<<')
					Loggers.Info('>>>>> ' + endCheckIpTimeFormat + '|' + title + u'|结束,抓取到' + str(len(avalibleIpsOneWeb)) + u'条可用ip,共耗时' + str(endCheckIpTime - startGetIpTime) + ' <<<<<')
					self.insert_data(Loggers, avalibleIpsOneWeb)
				except BaseException, e:
					Loggers.Error(u'>>>>> 请求url出错 ' + str(e) + '<<<<<')
			except BaseException, e:
				Loggers.Error(u'>>>>> 抓取ip循环出错 ' + str(e) + '<<<<<')
			time.sleep(10)
		
	def insert_data(self, Loggers, avalibleIps):
		cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		Loggers.Info('>>>>> ' + cur_time + u'|开始插入数据<<<<<')
		sql_select = "SELECT * FROM " + self.cfg.get("DB", "DBNAME") +".ipProxy WHERE ip = (%s) LIMIT 1"
		sql_update = "UPDATE " + self.cfg.get("DB", "DBNAME") + ".ipProxy SET power = (%s), update_time = (%s) WHERE ip = (%s)"
		sql_insert = "INSERT INTO " + self.cfg.get("DB", "DBNAME") + ".ipProxy (ip, power, time, source, create_time, update_time)"
		sql_insert += "VALUES (%s, %s, %s, %s, %s, %s)"
		try:
			for item in avalibleIps:
				hasOne = self.mysql.getOne(sql_select, item['ip'])
				if hasOne:
					self.mysql.update(sql_update, (str(int(hasOne['power']) + 1), cur_time, item['ip']))
					Loggers.Info(u'>>>>>更新ip:' + item['ip'] + u'-power从' + str(hasOne['power']) + u'更新至' + str(int(hasOne['power']) + 1)+ '<<<<<')
				else:
					self.mysql.insertOne(sql_insert, (item['ip'], '1', item['time'], item['source'], cur_time, cur_time))
					Loggers.Info(u'>>>>> 插入ip:' + item['ip'] + '<<<<<')
		except BaseException, e:
			Loggers.Error('>>>>> insert_data' + u' 出错' + e.message + '<<<<<')
		Loggers.Info(u'>>>>> 插入数据结束 <<<<<')
		self.mysql.end()
	
	def check_db_ip(self):
		mysql = Mysql(self.cfg.get('DB', 'DBHOST'), int(self.cfg.get('DB', 'DBPORT')), self.cfg.get('DB', 'DBUSER'), self.cfg.get('DB', 'DBPWD'), 3, 5)
		Loggers = Logger(special_log_file = 'checkDbIp')
		while 1 == 1:
			Loggers.Info(u'>>>>>开始检查数据库中已有ip<<<<<')
			sql_select = "SELECT * FROM " + self.cfg.get("DB", "DBNAME") +".ipProxy LIMIT 1000"
			sql_update = "UPDATE " + self.cfg.get("DB", "DBNAME") + ".ipProxy SET power = (%s), update_time = (%s) WHERE ip = (%s)"
			sql_delete = "DELETE FROM " + self.cfg.get("DB", "DBNAME") + ".ipProxy WHERE ip = (%s)"
			cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
			try:
				try:
					ipsFromDb = mysql.getMany(sql_select, 1000)
				except BaseException, e:
					Loggers.Error(u'>>>>>从数据取出所有ip出错' + e.message + '<<<<<')	
				Loggers.Info(u'>>>>>取出所有ip<<<<<')
				if ipsFromDb:
					for item in ipsFromDb:
						Loggers.Info(u'>>>>>检查'+str(item['ip'])+'|'+str(item['power'])+'<<<<<')
						result = self.utils.checkIpForAJK(item['ip'])
						power = int(item['power'])
						if result and result['move'] == 'add':
							powerNew = power + 1
							Loggers.Info(u'>>>>>更新ip:' + item['ip'] + '-power从' + str(power) + '更新至' + str(powerNew)+ '<<<<<')
							mysql.update(sql_update, (str(powerNew), cur_time, item['ip']))
						elif result and result['move'] == 'minus'and power > 1:
							powerNew = power - 1
							Loggers.Info(u'>>>>>更新ip:' + item['ip'] + '-power从' + str(power) + '更新至' + str(powerNew)+ '<<<<<')
							mysql.update(sql_update, (str(powerNew), cur_time, item['ip']))
						else:
							Loggers.Info(u'>>>>>删除ip:' + item['ip'] + '<<<<<')
							mysql.delete(sql_delete, (item['ip']))
						mysql.end()
			except BaseException, e:
				Loggers.Error('>>>>> check_db_ip ' + u'出错' + e.message + '<<<<<')
			Loggers.Info(u'>>>>>检查数据库ip结束<<<<<')
			time.sleep(60 * 10)

	def check_all_thread(self, funcs):
		while 1 == 1:
			try:
				Loggers = Logger(special_log_file = 'checkAllThread')
				Loggers.Info(u'>>>>> 开始检查所有线程 <<<<<')
				for fun in funcs:
					Loggers.Info(u'>>>>> 检查' + str(fun.getName()) + '线程 <<<<<')
					if not fun.isAlive():
						Loggers.Info(u'>>>>> ' + str(fun.getName()) + '线程停止，重新启动 <<<<<')
						fun.start()
					else:
						Loggers.Info(u'>>>>> ' + str(fun.getName()) + '线程运行中 <<<<<')
				time.sleep(60 * 60)
			except BaseException, e:
				Loggers.Error('>>>>> check_all_thread ' + u'出错' + e.message + ' <<<<<')

if __name__ == '__main__':
	ipProxys = ipProxy()
	try:
		get_ip_from_66ip = threading.Thread(target=ipProxys.get_ip_from_66ip)
		get_ip_from_ip3366 = threading.Thread(target=ipProxys.get_ip_from_ip3366)
		get_ip_from_xici = threading.Thread(target=ipProxys.get_ip_from_xici)
		check_db_ip = threading.Thread(target=ipProxys.check_db_ip)
		get_ip_from_66ip.setName('66ip')
		get_ip_from_ip3366.setName('ip3366')
		get_ip_from_xici.setName('xici')
		check_db_ip.setName('checkDbIp')
		check_all_thread = threading.Thread(target=ipProxys.check_all_thread, args=([get_ip_from_66ip, get_ip_from_ip3366, get_ip_from_xici, check_db_ip],))
		check_all_thread.start()
	except Exception,e:
		ipProxys.Loggers.Error("ipProxy [ERROR] :" + str(e))
