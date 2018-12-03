#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis

def write_test():
    r = redis.Redis(host='192.168.31.25', port=6379, db=0)
    r.set('name', 'zhangsan')   #添加
    print (r.get('name'))   #获取