#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests
import sys,os
from bs4 import BeautifulSoup
import re
import random
import time
from dbPool import Mysql
from util import Utils
reload(sys)
sys.setdefaultencoding('utf-8')
class ipProxy():

	user_agents = [
    "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
		"Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
		"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"
	]
		
	headers = {
		'Accept-Language': 'zh-CN,zh;q=0.9'
	}
	ip = '45.236.169.161:42181'
	def __init__(self):
		utils = Utils()
		self.cfg = utils.pathToConfig()
		self.mysql = Mysql(self.cfg.get('DB', 'DBHOST'), int(self.cfg.get('DB', 'DBPORT')), self.cfg.get('DB', 'DBUSER'), self.cfg.get('DB', 'DBPWD'), 3, 5)
		print('start get ip')

	def get_ips(self):
		try:
			head = self.headers
			url = 'https://wuhan.anjuke.com/sale/?from=navigation'
			proxies = {'http': self.ip, 'https': self.ip}
			head['user-agent'] = random.choice(self.user_agents)
			print(self.ip + '====' + head['user-agent'])
			r = requests.get(url,  timeout = 15, proxies = proxies, headers=head)
			soup = BeautifulSoup(r.text, "html.parser")
			title = soup.find('title').get_text()
			print(title)
			time.sleep(10)
		except BaseException,e:
			print(str(e))

	def insert_data(self):
		cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		# sql_select = "SELECT * FROM " + self.cfg.get("DB", "DBNAME") +".ipProxy"
		sql_update = "UPDATE " + self.cfg.get("DB", "DBNAME") + ".ipProxy SET power = (%s), update_time = (%s)"
		sql_insert = "INSERT INTO " + self.cfg.get("DB", "DBNAME") + ".ipProxy (ip, power, time, source, create_time, update_time)"
		sql_select = "SELECT * FROM " + self.cfg.get("DB", "DBNAME") +".houseConfig LIMIT 1"
		hasOne = self.mysql.getOne(sql_select)
		print(hasOne)

	def get_ip_from_ip3366(self):

		title = u'云代理'
		url = ['http://www.ip3366.net/free/','http://www.ip3366.net/free/?stype=1&page=2']
		head = self.headers
		head['user-agent'] = random.choice(self.user_agents)
		ips = []
		for u in url:
			r = requests.get(u, headers=head)
			soup = BeautifulSoup(r.text, "html.parser")
			list = soup.find('div', attrs={'id': 'list'}).find_all('td')

			for l in list:
				content = l.get_text().strip()
				if re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', content):
					strText = content
				if re.match(r'^([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{4}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$', content):
					strText = strText + ':' + content
					ips.append(strText)
		print(ips)

	def change_name(self):
		path = self.cfg.get('log_file', 'log')
		print(path)
		print(path+'.'+time.strftime("%Y%m%d%H%M%S", time.localtime()))
		os.rename(path, path+'.'+time.strftime("%Y%m%d%H%M%S", time.localtime()))
if __name__ == '__main__':
	ipProxys = ipProxy()
	# ipProxys.get_ips()
	# ipProxys.get_ip_from_ip3366()
	# ipProxys.change_name()
	ipProxys.insert_data()
