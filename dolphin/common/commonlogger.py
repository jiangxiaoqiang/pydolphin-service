# --encoding:utf-8--

import logging
import configparser
import logging.handlers
import os
import time

config = configparser.ConfigParser()
configFilePath = os.path.abspath("dolphin/config.ini")
with open(configFilePath, "r",encoding="utf-8") as cfgfile:
    config.readfp(cfgfile)


class commonlogger:
    def __init__(self):
        now_date_time = time.strftime('%Y-%m-%d',time.localtime())
        logFileName = "./dolphin/log/spider" + now_date_time + ".log"
        handler = logging.handlers.RotatingFileHandler(logFileName, maxBytes=1024 * 1024 * 1024,
                                                       backupCount=5)
        format = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        formatter = logging.Formatter(format)  # 实例化formatter
        handler.setFormatter(formatter)  # 为handler添加formatter
        self.logger = logging.getLogger('tst')  # 获取名为tst的logger
        self.logger.addHandler(handler)  # 为logger添加handler
        self.logger.setLevel(logging.DEBUG)

    def getlogger(self):
        return self.logger
