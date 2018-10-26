# -*- coding: utf-8 -*-
# for receive the iot remote unit
# ganben

# mysql 
# mem data structure

# redis
# for cacke/simple (no share with web) data not in mysql
# for complex data: use pickle as object storage/retrieve, with direct redis set/get
# example:
'''
obj = ExampleObject()
pickled_object = pickle.dumps(obj)
r.set('some_key', pickled_object)
unpacked_object = pickle.loads(r.get('some_key'))
obj == unpacked_object
'''

import sys
import struct
import json
import logging
import datetime
import pickle
import os
import time
import threading
import queue
import asyncio

import redis
import pygtrie
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

class WorkerThread(threading.Thread):
    """
    worker thread that takes redis live data to db
    """
    def __init__(self, iq, oq):
        super(WorkerThread, self).__init__()
        self.iq = iq
        self.oq = oq
        self.stoprequest = threading.Event()
    
    def run(self):
        # a time job here?
        #
        while not self.stoprequest.isSet():
            try:
                # blocking get with time out 0.05s
                t = 3600*24
                
                # time.sleep(t)
                job_in = self.iq.get(True, 0.05)
                if datetime.datetime.today() - job_in >= datetime.timedelta(minutes=10):
                    
                    job_out = self.process(job_in)
                    
                    self.iq.put(datetime.datetime.today())
                    try:
                        self.oq.put(job_out)
                    except asyncio.QueueFull:
                        self.oq.get()
                else:
                    # put back it to queue
                    self.iq.put(job_in)
                    time.sleep(3600)
                
            except queue.Empty:
                continue
    def process(self, job_in):
        # do nothing
        # TODO: update live data to sql
        # TODO: clear existing trie and refresh redis





        return 1
# data structure part
#SQL s from dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

INSERT_DEVICEDAILY = ("INSERT INTO stats_devicedaily "
                    "(date, sums, pin1, pin2, pin3, pin4, device_id)"
                    "VALUES (%s, %s, %d, %d, %d, %d, %d, %d)")

DEVICE_DATA = ()


# 1. active device data
class ActiveDevice:
    def __init__(self):
        self.active_length = 0
        self.device = {}  # k:device v: [total, pin1, pin2, pin3, pin4]
        #

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
    def feed(self, data):
        pass
        #to parse device to shop 


if __name__ == "__main__":
    # start multi threading
    in_queue = queue.Queue(maxsize=10)
    out_queue = queue.Queue(maxsize=100)
    # pool = [ WorkerThread(iq=in_queue,oq=out_queue) for i in range(2)]
    # for p in pool:
    #     time.sleep(100)
    #     p.start()
    t = WorkerThread(iq=in_queue, oq=out_queue)
    t.start()
