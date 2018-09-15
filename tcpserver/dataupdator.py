# -*- coding: utf-8 -*-
# for receive the iot remote unit
# ganben

# mysql 
# mem data structure

# redis
# for cacke/simple (no share with web) data not in mysql

import sys
import struct
import json
import logging
import datetime

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

# 1. active device
class ActiveDevice:
    def __init__(self, device_id):
        self.id = device_id
        self.on = datetime.datetime.now()
        self.active_length = 0
        self.last_msg = self.on
    def refresh(self, active_length):
        self.active_length = active_length
        self.last_msg = datetime.datetime.now()

    # TODO: serilizaer
    # TODO data model framework

# 2. pin signal
class LivePin:
    def __init__(self, device_id, pin_id):
        self.id = device_id
        self.pin = pin_id
    # TODO: 