#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests
import sys,os
from bs4 import BeautifulSoup
import ConfigParser,traceback
from util import Utils
from printLog import Logger
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

	ips = []
	avalibleIps = []

	def __init__(self):
		self.Logger = Logger(special_log_file = 'getProxy')
		self.user_agents = Headers().user_agents
		self.headers = Headers().headers
		self.cfg = self.utils.pathToConfig()
		self.mysql = Mysql(self.cfg.get('DB', 'DBHOST'), int(self.cfg.get('DB', 'DBPORT')), self.cfg.get('DB', 'DBUSER'), self.cfg.get('DB', 'DBPWD'), 3, 5)
	
	def get_ip_from_xici(self):
		avalibleIpsOneWeb = []
		startGetIpTime = time.time()
		startGetIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		title = u'西祠代理'
		self.Logger.Info('>>>>> ' + startGetIpTimeFormat + '|' + title + u'|开始抓取ip <<<<<')
		url = 'http://www.xicidaili.com/nn/'
		head = self.headers
		head['user-agent'] = random.choice(self.user_agents)
		r = requests.get(url, headers=head)
		soup = BeautifulSoup(r.text, "html.parser")
		list = soup.find('table', attrs={'id': 'ip_list'}).find_all('td')
		strText = ''
		self.ips = []
		for l in list:
			content = l.get_text().strip()
			if re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', content):
				strText = content
			if re.match(r'^([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{4}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$', content):
				strText = strText + ':' + content
				self.ips.append(strText)
		endGetIpTime = time.time()
		endGetIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		self.Logger.Info('>>>>> ' + endGetIpTimeFormat + '|' + title + u'|结束抓取ip,共抓取' + str(len(self.ips)) + '条 <<<<<')
		self.Logger.Info('>>>>> ' + endGetIpTimeFormat + '|' + title + u'|开始检查ip是否可用,抓取共耗时' + str(endGetIpTime - startGetIpTime) + ' <<<<<')

		for ip in self.ips:
			start = time.time()
			if self.utils.checkIpForAJK(ip):
				end = time.time()
				avalibleIpsOneWeb.append({
					'source': 'xici',
					'ip': ip,
					'time':str(end - start)
				})
		endCheckIpTime = time.time()
		endCheckIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		self.Logger.Info('>>>>> ' + endCheckIpTimeFormat + '|' + title + u'|结束检查ip是否可用,检查共耗时' + str(endCheckIpTime - endGetIpTime) + ' <<<<<')
		self.Logger.Info('>>>>> ' + title + u'|成功率:' + str(len(avalibleIpsOneWeb)) + '-' +str(len(self.ips)) + ' <<<<<')
		self.Logger.Info('>>>>> ' + endCheckIpTimeFormat + '|' + title + u'|结束,抓取到' + str(len(avalibleIpsOneWeb)) + '条可用ip,共耗时' + str(endCheckIpTime - startGetIpTime) + ' <<<<<')
		self.avalibleIps.append(avalibleIpsOneWeb)
	
	def get_ip_from_ip3366(self):
		avalibleIpsOneWeb = []
		startGetIpTime = time.time()
		startGetIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		title = u'云代理'
		self.Logger.Info('>>>>> ' + startGetIpTimeFormat + '|' + title + u'|开始抓取ip <<<<<')
		url = ['http://www.ip3366.net/free/','http://www.ip3366.net/free/?stype=1&page=2']
		# url = ['http://www.ip3366.net/free/']
		head = self.headers
		head['user-agent'] = random.choice(self.user_agents)
		self.ips = []
		for u in url:
			r = requests.get(u, headers=head)
			soup = BeautifulSoup(r.text, "html.parser")
			list = soup.find('div', attrs={'id': 'list'}).find_all('td')
			strText = ''
			for l in list:
				content = l.get_text().strip()
				if re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', content):
					strText = content
				if re.match(r'^([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{4}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$', content):
					strText = strText + ':' + content
					self.ips.append(strText)
		endGetIpTime = time.time()
		endGetIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		self.Logger.Info('>>>>> ' + endGetIpTimeFormat + '|' + title + u'|结束抓取ip,共抓取' + str(len(self.ips)) + '条 <<<<<')
		self.Logger.Info('>>>>> ' + endGetIpTimeFormat + '|' + title + u'|开始检查ip是否可用,抓取共耗时' + str(endGetIpTime - startGetIpTime) + ' <<<<<')

		for ip in self.ips:
			start = time.time()
			if self.utils.checkIpForAJK(ip):
				end = time.time()
				avalibleIpsOneWeb.append({
					'source': 'IP366',
					'ip': ip,
					'time':str(end - start)
				})
		endCheckIpTime = time.time()
		endCheckIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		self.Logger.Info('>>>>> ' + endCheckIpTimeFormat + '|' + title + u'|结束检查ip是否可用,检查共耗时' + str(endCheckIpTime - endGetIpTime) + ' <<<<<')
		self.Logger.Info('>>>>> ' + title + u'|成功率:' + str(len(avalibleIpsOneWeb)) + '-' +str(len(self.ips)) + ' <<<<<')
		self.Logger.Info('>>>>> ' + endCheckIpTimeFormat + '|' + title + u'|结束,抓取到' + str(len(avalibleIpsOneWeb)) + '条可用ip,共耗时' + str(endCheckIpTime - startGetIpTime) + ' <<<<<')
		self.avalibleIps.append(avalibleIpsOneWeb)

	def get_ip_from_66ip(self):
		avalibleIpsOneWeb = []
		startGetIpTime = time.time()
		title = u'安小莫'
		startGetIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		self.Logger.Info('>>>>> ' + startGetIpTimeFormat + '|' + title + u'|开始抓取ip <<<<<')
		url = 'http://www.66ip.cn/mo.php?sxb=&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=http%3A%2F%2Fwww.66ip.cn%2F%3Fsxb%3D%26tqsl%3D100%26ports%255B%255D2%3D%26ktip%3D%26sxa%3D%26radio%3Dradio%26submit%3D%25CC%25E1%2B%2B%25C8%25A1'
		head = self.headers
		head['user-agent'] = random.choice(self.user_agents)
		r = requests.get(url, headers=head)
		r.encoding = 'gb2312'
		p = r'(?:((?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5]))\D+?(6[0-5]{2}[0-3][0-5]|[1-5]\d{4}|[1-9]\d{1,3}|[0-9]))'
		iplist = re.findall(p,r.text)
		self.ips = []
		for item in iplist:
			self.ips.append(item[0] + ':' + item[1])
		endGetIpTime = time.time()
		endGetIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		self.Logger.Info('>>>>> ' + endGetIpTimeFormat + '|' + title + u'|结束抓取ip,共抓取' + str(len(self.ips)) + '条 <<<<<')
		self.Logger.Info('>>>>> ' + endGetIpTimeFormat + '|' + title + u'|开始检查ip是否可用,抓取共耗时' + str(endGetIpTime - startGetIpTime) + ' <<<<<')

		for ip in self.ips:
			start = time.time()
			if self.utils.checkIpForAJK(ip):
				end = time.time()
				avalibleIpsOneWeb.append({
					'source': '66ip',
					'ip': ip,
					'time':str(end - start)
				})
		endCheckIpTime = time.time()
		endCheckIpTimeFormat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		self.Logger.Info('>>>>> ' + endCheckIpTimeFormat + '|' + title + u'|结束检查ip是否可用,检查共耗时' + str(endCheckIpTime - endGetIpTime) + ' <<<<<')
		self.Logger.Info('>>>>> ' + title + u'|成功率:' + str(len(avalibleIpsOneWeb)) + '-' +str(len(self.ips)) + ' <<<<<')
		self.Logger.Info('>>>>> ' + endCheckIpTimeFormat + '|' + title + u'|结束,抓取到' + str(len(avalibleIpsOneWeb)) + '条可用ip,共耗时' + str(endCheckIpTime - startGetIpTime) + ' <<<<<')
		self.avalibleIps.append(avalibleIpsOneWeb)
		
	def insert_data(self):
		cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		self.Logger.Info('>>>>> ' + cur_time + u'|开始插入数据<<<<<')
		length = 0
		for l in self.avalibleIps:
			length += len(l)
		self.Logger.Info('>>>>> ' + cur_time + u'|开始插入数据, 共爬取' + str(len(self.avalibleIps))+'个网站,共抓取' + str(length) + '个可用ip<<<<<')
		sql_select = "SELECT * FROM " + self.cfg.get("DB", "DBNAME") +".ipProxy WHERE ip = (%s) LIMIT 1"
		sql_update = "UPDATE " + self.cfg.get("DB", "DBNAME") + ".ipProxy SET power = (%s), update_time = (%s) WHERE ip = (%s)"
		sql_insert = "INSERT INTO " + self.cfg.get("DB", "DBNAME") + ".ipProxy (ip, power, time, source, create_time, update_time)"
		sql_insert += "VALUES (%s, %s, %s, %s, %s, %s)"
		try:
			for items in self.avalibleIps:
				for item in items:
					hasOne = self.mysql.getOne(sql_select, item['ip'])
					if hasOne:
						self.mysql.update(sql_update, (str(int(hasOne['power']) + 1), cur_time, item['ip']))
						self.Logger.Info(u'>>>>>更新ip:' + item['ip'] + '-power从' + str(hasOne['power']) + '更新至' + str(int(hasOne['power']) + 1)+ '<<<<<')
					else:
						self.mysql.insertOne(sql_insert, (item['ip'], '1', item['time'], item['source'], cur_time, cur_time))
		except BaseException, e:
			self.Logger.Error('>>>>> insert_data' + u' 出错' + e.message + '<<<<<')
		self.Logger.Info(u'>>>>> 插入数据结束 <<<<<')
		self.mysql.end()
	
	def check_db_ip(self):
		self.Logger.Info(u'>>>>>开始检查数据库中已有ip<<<<<')
		sql_select = "SELECT * FROM " + self.cfg.get("DB", "DBNAME") +".ipProxy"
		sql_update = "UPDATE " + self.cfg.get("DB", "DBNAME") + ".ipProxy SET power = (%s), update_time = (%s) WHERE ip = (%s)"
		sql_delete = "DELETE FROM " + self.cfg.get("DB", "DBNAME") + ".ipProxy WHERE ip = (%s)"
		cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		try:
			ipsFromDb = self.mysql.getMany(sql_select, 1000)
			if ipsFromDb:
				for item in ipsFromDb:
					if self.utils.checkIpForAJK(item['ip']):
						power = int(item['power'])
						powerNew = power + 1
						self.Logger.Info(u'>>>>>更新ip:' + item['ip'] + '-power从' + str(power) + '更新至' + str(powerNew)+ '<<<<<')
						self.mysql.update(sql_update, (str(powerNew), cur_time, item['ip']))
					else:
						self.Logger.Info(u'>>>>>删除ip:' + item['ip'] + '<<<<<')
						self.mysql.delete(sql_delete, (item['ip']))
		except BaseException, e:
			self.Logger.Error('>>>>> check_db_ip ' + u'出错' + e.message + '<<<<<')
		self.Logger.Info(u'>>>>>检查数据库ip结束<<<<<')
		self.mysql.end()

	def get_insert_ip(self):
		self.Logger.Info(u'>>>>> ================== 开始抓取ip ==================<<<<<')
		self.avalibleIps = []
		self.check_db_ip()
		self.get_ip_from_66ip()
		# print(self.avalibleIps)
		self.get_ip_from_ip3366()
		self.get_ip_from_xici()
		# print(self.avalibleIps)
		self.insert_data()
		self.Logger.Info(u'>>>>> 可用ip:' + str(self.avalibleIps) + '<<<<<')
		self.Logger.Info(u'>>>>> ================== 抓取ip结束 ================== <<<<<')


if __name__ == '__main__':
	ipProxys = ipProxy()
	while 1==1:
		try:
			ipProxys.get_insert_ip()
		except Exception,e:
			ipProxys.Logger.Error("ipProxy [ERROR] :" + str(e))
