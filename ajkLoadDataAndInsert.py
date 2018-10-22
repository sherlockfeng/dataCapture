# -*- coding: utf8 -*-
import requests
import sys,os
from bs4 import BeautifulSoup
import json,time,threading
from printLog import Logger
import ConfigParser,traceback
from dbPool import Mysql
import random
from util import Utils
from headerConfig import Headers
import schedule
reload(sys)
sys.setdefaultencoding('utf-8')

class ajkLoadDataAndInsert():
	city_list = []
	user_agents = []
	headers = {}
	utils = Utils()
	list_data = []
	ips = []
	ipIndex = 0
	ip = {}

	def __init__(self):
		self.Logger = Logger('getAjkData')
		self.user_agents = Headers().user_agents
		self.headers = Headers().headers
		self.cfg = self.utils.pathToConfig()
		self.mysql = Mysql(self.cfg.get('DB', 'DBHOST'), int(self.cfg.get('DB', 'DBPORT')), self.cfg.get('DB', 'DBUSER'), self.cfg.get('DB', 'DBPWD'), 3, 5)

	def get_city_sec_url(self):
		self.Logger.Info(u'>>>>> 获取需要抓取二手房房价的城市列表 <<<<<')
		sql_select = "SELECT * FROM " + self.cfg.get("DB", "DBNAME") +".houseConfig WHERE active_ajk_sec = 1"
		try:
			self.city_list = self.mysql.getMany(sql_select, 100)
		except BaseException, e:
			self.Logger.Error(u'>>>>> get_city_sec_url ' + u'出错' + str(e) + '<<<<<')
		self.Logger.Info(u'>>>>> 获取需要抓取二手房房价的城市列表结束' + str(self.city_list) + ' <<<<<')
	
	def get_ips(self):
		self.Logger.Info(u'>>>>> 获取可用ip列表 <<<<<')
		sql_select = "SELECT * FROM " + self.cfg.get("DB", "DBNAME") +".ipProxy ORDER BY power desc, update_time desc"
		try:
			self.ips = self.mysql.getMany(sql_select, 100)
		except BaseException, e:
			self.Logger.Error(u'>>>>> get_ip ' + u'出错' + str(e) + '<<<<<')
		self.Logger.Info(u'>>>>> 获取可用ip列表结束' + str(self.ips) + ' <<<<<')
		
	def load_detail_info_sec(self):
		self.Logger.Info(u'>>>>> 开始抓取详细数据 <<<<<')
		self.ip = self.ips[0]
		for city in self.city_list:
			self.Logger.Info(u'>>>>> 开始抓取:' + city['city_name'] + '|url:' + str(city['ajk_sec_url']) + '|ip:' + self.ip['ip'] + '<<<<<')
			oneCityGetDown = True
			while oneCityGetDown:
				try:
					self.Logger.Info(u'>>>>> 使用ip:' + str(self.ip['ip']) + '<<<<<')
					proxies = {'http': self.ip['ip'], 'https': self.ip['ip']}
					head = self.headers
					head['user-agent'] = random.choice(self.user_agents)
					r = requests.get(city['ajk_sec_url'],	timeout = 10, proxies = proxies, headers=head)
					time.sleep(random.random() * 10)
					soup = BeautifulSoup(r.text, "html.parser")
					title = soup.find('title').get_text()
					if '二手房' in title:
						self.Logger.Info(u'>>>>> ip:' + str(self.ip['ip']) + u'可用|' + title + '<<<<<')
						list = soup.find(attrs={'id': 'houselist-mod-new'}).find_all('li')
						for l in list[0:]:
							oneDetailGetDown = True
							while oneDetailGetDown:
								house_title = l.find(attrs={'class': 'house-title'}).find('a').attrs['title'].strip()
								price = l.find(attrs={'class': 'price-det'}).get_text().strip()
								try:
									detail_url = l.find(attrs={'class': 'house-title'}).find('a').attrs['href']
									self.Logger.Info(u'>>>>> 开始抓取:' + house_title + '|' + detail_url.split('view/')[1].split('?')[0] + '|ip:' + self.ip['ip'] + u'|数据<<<<<')
									proxies = {'http': self.ip['ip'], 'https': self.ip['ip']}
									head['user-agent'] = random.choice(self.user_agents)
									r_detail = requests.get(detail_url.split('now_time')[0],	timeout = 10, proxies = proxies, headers=head)
									time.sleep(random.random() * 20)
									soup_detail = BeautifulSoup(r_detail .text, "html.parser")
									title_detail = soup_detail.find('title').get_text()
									if '58安居客' in title_detail and '验证' not in title_detail:
										try:
											self.Logger.Info(u'>>>>> 开始从列表页获取详情中需要的数据|'+ title_detail+'<<<<<')
											detail_dict = self.get_data(soup_detail)
											detail_dict['city_id'] = city['city_id']
											detail_dict['city_name'] = city['city_name']
											detail_dict['source'] = 'ajk'
											detail_dict['house_id'] = detail_url.split('view/')[1].split('?')[0]
											detail_dict['link_url'] = detail_url.split('?')[0]
											detail_dict['title'] = house_title
											detail_dict['price'] = price
											oneDetailGetDown = False
											self.insert_update_data(detail_dict)
										except BaseException,e:
											self.Logger.Info(u'>>>>> 从列表页获取详情中需要的数据出错' + str(e) + '<<<<<')
									else:
										self.Logger.Info(u'>>>>> ip for detail:' + str(self.ip['ip']) + u'不可用|' + str(title_detail) + '<<<<<')
										self.ip = self.get_active_ip()
								except BaseException,e:
									self.Logger.Info(u'>>>>> ip for detail:' + str(self.ip['ip']) + u'不可用,超时|' + str(e) + '<<<<<')
									self.ip = self.get_active_ip()
						oneCityGetDown = False
						self.Logger.Info(u'>>>>> city:' + city['city_name'] + u'抓取完成<<<<<')
					else:
						self.Logger.Info(u'>>>>> ip:' + str(self.ip['ip']) + u'不可用|' + title + '<<<<<')
						self.ip = self.get_active_ip()
				except BaseException,e:
					self.Logger.Info(u'>>>>> ip:' + str(self.ip['ip']) + u'不可用,超时|' + str(e) + '<<<<<')
					self.ip = self.get_active_ip()

	def get_data(self, soup):
		self.Logger.Info(u'>>>>> 开始解析详情页表格数据<<<<<')
		detail_dict = {}
		try:
			detail_info = soup.find(attrs={'class': 'houseInfo-detail-list'})
			self.Logger.Info('detail_info')
			detail_dict['uni_price'] = ''
			detail_dict['house_type'] = ''
			detail_dict['house_floor'] = ''
			detail_dict['build_time'] = ''
			detail_dict['address'] = ''
			detail_dict['community'] = ''
			detail_dict['property_year'] = ''
			detail_dict['property_type'] = ''
			detail_dict['floor_area'] = ''
			detail_dict['face_to'] = ''
			detail_dict['elevator'] = ''
			detail_dict['down_payments'] = ''
			detail_dict['monthly_supply'] = ''
			detail_dict['decoration'] = ''
			detail_dict['describes'] = ''

			if detail_info.find('div', text='房屋单价：'):
				detail_dict['uni_price'] = detail_info.find('div', text='房屋单价：').find_next('div').get_text().strip()
				self.Logger.Info('uni_price')

			if detail_info.find('div', text='房屋户型：'):
				detail_dict['house_type'] = detail_info.find('div', text='房屋户型：').find_next('div').get_text().strip()
				self.Logger.Info('house_type')

			if detail_info.find('div', text='所在楼层：'):
				detail_dict['house_floor'] = detail_info.find('div', text='所在楼层：').find_next('div').get_text().strip()
				self.Logger.Info('house_floor')

			if detail_info.find('div', text='建造年代：'):
				detail_dict['build_time'] = detail_info.find('div', text='建造年代：').find_next('div').get_text().strip()
				self.Logger.Info('build_time')

			if detail_info.find('div', text='所在位置：'):
				detail_dict['address'] = detail_info.find('div', text='所在位置：').find_next('div').get_text().strip()
				self.Logger.Info('address')

			if detail_info.find('div', text='所属小区：'):
				detail_dict['community'] = detail_info.find('div', text='所属小区：').find_next('div').get_text().strip()
				self.Logger.Info('community')
				
			if detail_info.find('div', text='建筑面积：'):
				detail_dict['floor_area'] = detail_info.find('div', text='建筑面积：').find_next('div').get_text().strip()
				self.Logger.Info('floor_area')

			if detail_info.find('div', text='房屋朝向：'):
				detail_dict['face_to'] = detail_info.find('div', text='房屋朝向：').find_next('div').get_text().strip()
				self.Logger.Info('face_to')

			if detail_info.find('div', text='装修程度：'):
				detail_dict['decoration'] = detail_info.find('div', text='装修程度：').find_next('div').get_text().strip()
				self.Logger.Info('decoration')

			if detail_info.find('div', text='配套电梯：'):
				detail_dict['elevator'] = detail_info.find('div', text='配套电梯：').find_next('div').get_text().strip()
				self.Logger.Info('elevator')

			if detail_info.find('div', text='产权性质：'):
				detail_dict['property_type'] = detail_info.find('div', text='产权性质：').find_next('div').get_text().strip()
				self.Logger.Info('property_type')

			if detail_info.find('div', text='产权年限：'):
				detail_dict['property_year'] = detail_info.find('div', text='产权年限：').find_next('div').get_text().strip()
				self.Logger.Info('property_year')

			if detail_info.find('div', text='参考首付：'):
				detail_dict['down_payments'] = detail_info.find('div', text='参考首付：').find_next('div').get_text().strip()
				self.Logger.Info('down_payments')

			if detail_info.find(attrs={'id': 'reference_monthpay'}):
				detail_dict['monthly_supply'] = detail_info.find(attrs={'id': 'reference_monthpay'}).get_text().strip()
				self.Logger.Info('monthly_supply')

			if soup.find_all('div', attrs={'class':'houseInfo-item-desc'}):
				detail_describe = soup.find_all('div', attrs={'class':'houseInfo-item-desc'})
				self.Logger.Info('detail_describe')
				self.Logger.Info(detail_describe)
				ser_l = detail_describe[0].get_text().strip() + '|' + detail_describe[1].get_text().strip() + '|' + detail_describe[2].get_text().strip()
				detail_dict['describes'] = ser_l

			self.Logger.Info(u'>>>>> 解析详情页表格数据解析成功<<<<<')
		except BaseException,e:
			self.Logger.Info(u'>>>>> 解析详情页表格数据解析出错' + str(e) + '<<<<<')
		return detail_dict

	def insert_update_data(self, detail_dict):
		self.Logger.Info(u'>>>>> 开始插入数据' + detail_dict['city_name'] + '|' + detail_dict['title'] + '|' + detail_dict['house_id'] + '<<<<<')
		sql_insert = "INSERT INTO " + self.cfg.get("DB", "DBNAME") +".houseSecOuterData (city_id,source,city_name,house_id,title,price,uni_price,house_type,house_floor,build_time,address,community,floor_area,face_to,decoration,elevator,property_type,property_year,down_payments,monthly_supply,link_url,describes,create_time,update_time)"
		sql_insert += " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		sql_select = "SELECT * FROM " + self.cfg.get("DB", "DBNAME") +".houseSecOuterData WHERE house_id = (%s) ORDER BY id DESC"
		sql_update = "UPDATE " + self.cfg.get("DB", "DBNAME") + ".houseSecOuterData SET title = (%s), price = (%s), uni_price = (%s),house_type = (%s), house_floor = (%s), build_time = (%s), address = (%s), community = (%s), floor_area = (%s), face_to = (%s), decoration = (%s), elevator = (%s), property_type = (%s), property_year = (%s), down_payments = (%s), monthly_supply = (%s), link_url = (%s), describes = (%s), update_time = (%s)"
		try:
			if self.mysql.getOne(sql_select, detail_dict['house_id']):
				self.Logger.Info(u'>>>>> 查询到|已有|' + detail_dict['city_name'] + '|' + detail_dict['title'] + '|' + detail_dict['house_id'] + '<<<<<')
				value = (detail_dict['title'], detail_dict['price'], detail_dict['uni_price'], detail_dict['house_type'], detail_dict['house_floor'], detail_dict['build_time'], detail_dict['address'], detail_dict['community'], detail_dict['floor_area'], detail_dict['face_to'], detail_dict['decoration'], detail_dict['elevator'], detail_dict['property_type'], detail_dict['property_year'], detail_dict['down_payments'], detail_dict['monthly_supply'], detail_dict['link_url'], detail_dict['describes'], cur_time)
				self.mysql.update(sql_update, value)
				self.Logger.Info(u'>>>>> 更新' + detail_dict['city_name'] + '|' + detail_dict['title'] + '|' + detail_dict['house_id'] + '成功<<<<<') 
			else:
				self.Logger.Info(u'>>>>> 查询到|没有|' + detail_dict['city_name'] + '|' + detail_dict['title'] + '|' + detail_dict['house_id'] + '<<<<<')
				value = (detail_dict['city_id'], detail_dict['source'], detail_dict['city_name'], detail_dict['house_id'], detail_dict['title'], detail_dict['price'], detail_dict['uni_price'], detail_dict['house_type'], detail_dict['house_floor'], detail_dict['build_time'], detail_dict['address'], detail_dict['community'], detail_dict['floor_area'], detail_dict['face_to'], detail_dict['decoration'], detail_dict['elevator'], detail_dict['property_type'], detail_dict['property_year'], detail_dict['down_payments'], detail_dict['monthly_supply'], detail_dict['link_url'], detail_dict['describes'], cur_time, cur_time)
				self.mysql.insertOne(sql_insert, value)
				self.Logger.Info(u'>>>>> 插入' + detail_dict['city_name'] + '|' + detail_dict['title'] + '|' + detail_dict['house_id'] + '成功<<<<<') 
		except BaseException, e:
			self.Logger.Error(u'>>>>> 插入' + detail_dict['city_name'] + '|' + detail_dict['title'] + '|' + detail_dict['house_id'] + u'出错 <<<<<' + str(e))
		self.mysql.end()

	def get_active_ip(self):
		if self.ipIndex < (len(self.ips) - 1):
			self.ipIndex += 1
		else:
			self.ipIndex = 0
			self.get_ips()
		time.sleep(10)
		return self.ips[self.ipIndex]

	def start(self):
		try:
			self.Logger.Info(u'>>>>> =============== 开始抓取数据 =============== <<<<<')
			self.get_city_sec_url()
			self.get_ips()
			self.load_detail_info_sec()
		except Exception,e:
			self.Logger.Error(u'>>>>> load_data_ajk main [Error] :' + str(e))
		
		
			

if __name__ == '__main__':
	loadData = ajkLoadDataAndInsert()
	schedule.every().day.at('08:00').do(loadData.start)
	while 1 == 1:
		schedule.run_pending()
		time.sleep(1)

