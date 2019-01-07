# --encoding:utf-8--

import os
import configparser

config = configparser.ConfigParser()
parentDirPath=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
with open(parentDirPath + "/config.ini", "r",encoding="utf-8") as cfgfile:
    config.readfp(cfgfile)

class confighelper:
    def __init__(self):
        return
        
    def init(self):
      return ''' host='%s',user='%s',passwd='postgres',db='dolphin',port=5432 ''' % ('35.194.196.172','postgres')

    def getValue(self,schema, key):
        return config.get(schema, key)

    def getGloabalValue(self, key):
        return config.get('global', key)
