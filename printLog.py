# -*- coding: utf8 -*-
import os,logging
import logging.config
import ConfigParser
from datetime import datetime,date,timedelta

class Logger():

    def __init__(self, special_log_file=None):
        self.conf = ConfigParser.ConfigParser()
        self.conf.read('./config.cfg')
        if special_log_file is None:
            SERVICE_NAME = self.conf.get("log", "SERVICE_NAME")
        else:
            SERVICE_NAME = special_log_file
        LOG_LEVEL = self.conf.get("log", "LOG_LEVEL")
        LOG_FILE_PATH = self.conf.get("log", "LOG_FILE_PATH")
        RUN_TYPE = self.conf.get("log", "RUN_TYPE")

        # 创建一个logger    
        self.logger = logging.getLogger(LOG_FILE_PATH+'/'+SERVICE_NAME)
        # CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
        self.logger.setLevel(LOG_LEVEL.upper())


        if RUN_TYPE.upper() == 'DEV':
            log_full_file_path = LOG_FILE_PATH+'/'+SERVICE_NAME+'.log'
        if RUN_TYPE.upper() == 'PRO':
            log_full_file_path = LOG_FILE_PATH+'/'+SERVICE_NAME+'.log'

        if not self.logger.handlers:
            # 创建一个handler，用于写入日志文件
            fh = logging.handlers.TimedRotatingFileHandler(log_full_file_path,'midnight')

            # 定义handler的输出格式formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            # fh.handlers.TimedRotatingFileHandler(log_full_file_path,'M',1,0)
            # fh.suffix = "%Y%m%d-%H%M.log"
            #定义一个filter
            #filter = logging.Filter('mylogger.child1.child2')
            #fh.addFilter(filter)
            # 给logger添加handler
            #logger.addFilter(filter)
            self.logger.addHandler(fh)
            

            if RUN_TYPE.upper() == 'DEV':
                # 再创建一个handler，用于输出到控制台    
                ch = logging.StreamHandler()
                ch.setFormatter(formatter)
                self.logger.addHandler(ch)

    def Info(self,content):
        self.logger.info(content)

    def Debug(self,content):
        self.logger.debug(content)

    def Warn(self,content):
        self.logger.warn(content)

    def Error(self,content):
        self.logger.error(content)
    def Close(self):
        self.logger.close()

    def Critical(self,content):
        self.logger.critical(content)







