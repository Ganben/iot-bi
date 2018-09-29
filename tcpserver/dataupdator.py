# -*- coding: utf-8 -*-
# for receive the iot remote unit
# ganben

# mysql 
# mem data structure

# redis
# for cacke/simple (no share with web) data not in mysql
# for complex data: use pickle as object storage/retrieve, with direct redis set/get

import sys
import struct
import json
import logging
import datetime
import pickle

import redis
# from paho.mqtt import client
import mysql.connector 

### set up logging
logger = logging.getLogger('dataupdator')
logger.setLevel(logging.DEBUG)

# fh
fh = logging.FileHandler('dataupdator.log')
fh.setLevel(logging.DEBUG)
# ch
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

### MYSQL/DATAMODEL part
db = mysql.connector.connect(
    user='root',
    password = '123456',
    host = '127.0.0.1',
    database = 'iotbt',
    charset = 'utf8mb4'
)

# rd = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
rpool = redis.ConnectionPool(host='localhost', port=6379, db=0)
rd = redis.Redis(connection_pool=rpool)

# a multithread to scheduled job every some time;
class Timedjob:
    def __init__(self, inte):
        self.interval = inte
        self.last = datetime.datetime.now()
    
    def doit(self, datatable):
        if datetime.datetime.now() - self.last < self.interval:
            return
        else:
            self.last = datetime.datetime.now()
            self.update(datatable)
    
    def update(self, datatable):
        pass
        # TODO:do some query

# a multithreader
class DaemonThreader:
    def execute(self):
        pass
        # loop forever
        # wake every 1/4 minimun interval and do all job
        
    def addajob(self, job):
        pass
    
# data structure part

# 1. active device data
class ActiveDevice:
    def __init__(self):
        self.active_length = 0
        self.device = {}  # k:device v: [total, pin1, pin2, pin3, pin4]

# data manipulator class
class ActiveManager(object):
    def __init__(self):
        self.active_device = ActiveDevice()
        # load from redis if exist

    def feed(self, registration):
        pass # parse hex to registrated device, numbers

# 2. device-pin total data
class IndexLive:
    def __init__(self):
        self.devices = {}    # k = device v = incremented numbers
        # load from redis if exist

# data manipulator class
class IndexManager(object):
    def __init__(self):
        self.indexlive = IndexLive()
        # load from redis
    def feed(self, activedevices):
        pass

# 3. device-shop info map
class DevShopMap:
    def __init__(self):
        self.devices = {}  # k:dev, v:shop

class DevShopMapManager(object):
    def __init__(self):
        self.map = DevShopMap()
        # load from redis
        # and save to redis