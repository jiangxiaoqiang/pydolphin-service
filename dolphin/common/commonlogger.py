# --encoding:utf-8--

import logging
import configparser
import os
import time

config = configparser.ConfigParser()
configFilePath = os.path.abspath("dolphin/config.ini")
with open(configFilePath, "r",encoding="utf-8") as cfgfile:
    config.readfp(cfgfile)


class commonlogger:
    def __init__(self):
        log_file_path = "./dolphin/log"
        is_exists = os.path.exists(log_file_path)
        if not is_exists:
            os.mkdir(log_file_path)
        now_date_time = time.strftime('%Y-%m-%d',time.localtime())
        log_filename = "./dolphin/log/spider" + now_date_time + ".log"
        handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=1024 * 1024 * 100,
                                                       backupCount=2)
        log_format = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        formatter = logging.Formatter(log_format)
        handler.setFormatter(formatter)  
        self.logger = logging.getLogger('tst')  
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def getlogger(self):
        return self.logger
