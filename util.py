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
from printLog import Logger
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
    self.Logger = Logger()
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
    self.Logger.Info("now ip: " + ipaddr)
    if ipaddr == '10.246.104.17':
      self.cfg.read("./config.cfg")
    else:
      self.cfg.read("./config_online.cfg")
    return self.cfg
  
  def checkIpForAJK(self,ip):
    result = False
    try:
      url = 'https://wuhan.anjuke.com/sale/?from=navigation'
      proxies = {'http': ip, 'https': ip}
      head = self.headers
      head['user-agent'] = random.choice(self.user_agents)
      print(ip + '====' + head['user-agent'] + '/n')
      r = requests.get(url,  timeout = 10, proxies = proxies, headers=head)
      soup = BeautifulSoup(r.text, "html.parser")
      title = soup.find('title').get_text()
      if '武汉二手房' in title:
        result = True
    except BaseException,e:
      print(e.message)
    time.sleep(random.random() * 10)
    return result

if __name__ == '__main__':
  print('main')
