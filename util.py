# -*- coding: utf8 -*-
#-------------------------------------------------------------------------------
# Name:        工具类
# Purpose:
#
# Author:      heyunfeng
#
# PythonVersion: 2.7
#
# Created:     1/06/2018
# Copyright:   (c) heyunfeng 2018
# Licence:     <MIT>
#-------------------------------------------------------------------------------
import socket
import ConfigParser,traceback
import re
import random
import time
import requests
from bs4 import BeautifulSoup
from headerConfig import Headers
#-------------------------------------------------------------------------------
class Utils():

  user_agents = []
  headers = {}

  def __init__(self):
    self.cfg = ConfigParser.ConfigParser()
    self.user_agents = Headers().user_agents
    self.headers = Headers().headers

  def pathToConfig(self):
    """
    根据环境读取配置
    10.246.104.17
    """
    hostName = socket.gethostname()
    ipaddr = socket.gethostbyname(hostName)
    # if ipaddr == '10.246.104.17':
    #   self.cfg.read("./config.cfg")
    # else:
    self.cfg.read("./config.cfg")
    return self.cfg
  
  def checkIpForAJK(self,ip):
    result = {}
    try:
      url = 'https://wuhan.anjuke.com/sale/?from=navigation'
      proxies = {'http': ip, 'https': ip}
      head = self.headers
      head['user-agent'] = random.choice(self.user_agents)
      print(ip + '====' + head['user-agent'] + '/n')
      r = requests.get(url, timeout = 10, proxies = proxies, headers=head)
      soup = BeautifulSoup(r.text, "html.parser")
      title = soup.find('title').get_text()
      if '武汉二手房' in title:
        result = {"move": "add"}
      else:
        result = {"move": "minus"}
    except BaseException,e:
      print(e.message)
    time.sleep(random.random() * 10)
    return result

  def get_city_sec_url(self, Loggers, columeName, mysql):
    city_list = []
    Loggers.Info(u'>>>>> 获取需要抓取二手房房价的城市列表 <<<<<')
    sql_select = "SELECT * FROM " + self.cfg.get("DB", "DBNAME") +".houseConfig WHERE " + str(columeName) + " = 1"
    try:
            city_list = mysql.getMany(sql_select, 100)
    except BaseException, e:
            Loggers.Error(u'>>>>> get_city_sec_url ' + u'出错' + str(e) + '<<<<<')
    Loggers.Info(u'>>>>> 获取需要抓取二手房房价的城市列表结束' + str(city_list) + ' <<<<<')
    return city_list
    
  def get_ips(self, Loggers, ipName, mysql):
    ips = []
    Loggers.Info(u'>>>>> 获取可用ip列表 <<<<<')
    sql_select = "SELECT * FROM " + self.cfg.get("DB", "DBNAME") +"." + str(ipName) + " ORDER BY power desc, update_time desc"
    try:
        ips = mysql.getMany(sql_select, 100)
    except BaseException, e:
        Loggers.Error(u'>>>>> get_ip ' + u'出错' + str(e) + '<<<<<')
    Loggers.Info(u'>>>>> 获取可用ip列表结束' + str(ips) + ' <<<<<')
    return ips

  def get_active_ip(self, ips, ip, Loggers, ipName, mysql):
    active_ip = {}
    index = ips.index(ip)
    if int(index + 1) < len(ips):
      ips_return = ips
      active_ip = ips[index + 1]
    else:
      ips_return = self.get_ips(Loggers, ipName, mysql)
      active_ip = ips[0]
    return {"ips": ips_return, "active_ip": active_ip}

  def str_to_num(self, strtonum):
    if re.findall(r"\d*\.?\d*", strtonum)[0]:
      return re.findall(r"\d*\.?\d*", strtonum)[0]
    else:
      return '0'


if __name__ == '__main__':
  print('main')
