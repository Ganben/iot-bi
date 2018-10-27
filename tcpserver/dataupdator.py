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
import unittest

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

class WorkerThread(threading.Thread):
    """
    worker thread that takes redis live data to db
    """
    def __init__(self, iq, oq):
        super(WorkerThread, self).__init__()
        self.iq = iq
        self.oq = oq
        logger.debug('thread start')
        self.stoprequest = threading.Event()
    
    def run(self):
        # a time job here?
        #
        while not self.stoprequest.isSet():
            try:
                # blocking get with time out 0.05s
                t = 3600*24
                logger.debug('--thread run--')
                # time.sleep(t)
                job_in = self.iq.get(True, 0.05)
                if datetime.datetime.today() - job_in >= datetime.timedelta(hours=24):
                    logger.debug('--time compare ok --')
                    job_out = self.process(job_in)
                    
                    self.iq.put(datetime.datetime.today())
                    try:
                        self.oq.put(job_out)
                    except asyncio.QueueFull:
                        self.oq.get()
                else:
                    # put back it to queue
                    self.iq.put(job_in)
                    t = 3600*4 # interval: 4h
                    logger.debug('thread wait for %ss' % t)
                    time.sleep(t)
                
            except queue.Empty:
                logger.info('--thread queue empty exception--')
                continue
    def process(self, job_in):
        # do nothing
        # TODO: update live data to sql
        # TODO: clear existing trie and refresh redis
        logger.debug('--process job in at:%s--' % job_in)
        devices = load_rd_devices()
        shops = load_rd_shop()
        for e in devices:
            generate_dev_daily(e)
        for e in shops:
            generate_shop_daily(e)
        clear_rd_device()
        clear_rd_shop()
        logger.debug('--process end with db commit--')
        # the commit success, pk id is auto added ;
        db.commit()
        return 1
# data structure part
#SQL s from dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

QUERY_DEVICE_BY_ID = (
    "SELECT id, visited, status, shop_id, activated from stats_device "
    "WHERE id = %s "
)

QUERY_SHOP_BY_ID = (
    "SELECT id, name, units, counts FROM stats_shop "
    "WHERE id = %s "
)

INSERT_DEVICEDAILY = ("INSERT INTO stats_devicedaily "
                    "(date, sums, pin1, pin2, pin3, pin4, device_id)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)")

DEVICE_DATA = ()

INSERT_SHOPDAILY = (
    "INSERT INTO stats_shopdaily "
    "(date, sums, shop_id)"
    "VALUES (%s, %s, %s)"
)

SHOP_DATA = ()

def load_rd_devices():
    # load redis trie data
    # return list of devices
    res = []
    rkey = 'livedevicechart'
    o = pickle.loads(rd.get(rkey))
    d = datetime.date.today()
    for k, v in o.items():
        # get all
        if v['sum'] > -1:
            res.append(
                (
                    d, 
                    v['sum'],
                    v['stats'][0],
                    v['stats'][1],
                    v['stats'][2],
                    v['stats'][3],
                    v['label']
                )
            )
            # the format is for INSERT SQL sentences
    return res

def load_rd_shop():
    # load redis trie data
    # return list of shops
    res = []
    rkey = 'liveshopchart'
    o = pickle.loads(rd.get(rkey))
    d = datetime.date.today()
    for k, v in o.items():
        # get all 
        res.append((
            d,
            v['sum'],
            v['id']
        ))
        # the format is for INSERT SQL sentences
    return res

def generate_dev_daily(device):
    # a device dict input
    # generate the data model
    # execute insert of the generated data to mysql
    cursor = db.cursor()
    logger.debug('--paras len:%s' % len(device))
    cursor.execute(INSERT_DEVICEDAILY, device)
    res = cursor.lastrowid
    cursor.close()
    logger.debug('sql dev daily insert: %s' % res)
    return res

def generate_shop_daily(shop):
    # a shop dict input
    # generate the data model
    # execute insert of the data to mysql
    cursor = db.cursor()
    cursor.execute(INSERT_SHOPDAILY, shop)
    res = cursor.lastrowid
    cursor.close()
    logger.debug('sql shop daily insert: %s' % res)
    return res

def clear_rd_device():
    # clear the redis device data
    
    rkey = 'livedevicechart'
    o = pickle.loads(rd.get(rkey))
    for k, v in o.items():
        v['sum'] = 0
        v['stats'] = [0,0,0,0]
    rd.set(rkey, pickle.dumps(o))

    return 1

def clear_rd_shop():
    # clear the redis shop data
    
    rkey = 'liveshopchart'
    o = pickle.loads(rd.get(rkey))
    for k, v in o.items():
        v['sum'] = 0
        for i in v['data']:
            i = 0
    rd.set(rkey, pickle.dumps(o))
    
    return 1

if __name__ == "__main__":
    # start multi threading
    in_queue = queue.Queue(maxsize=10)
    out_queue = queue.Queue(maxsize=100)
    # pool = [ WorkerThread(iq=in_queue,oq=out_queue) for i in range(2)]
    # for p in pool:
    #     time.sleep(100)
    #     p.start()
    jobin = datetime.datetime.today()
    in_queue.put(jobin)
    t = WorkerThread(iq=in_queue, oq=out_queue)
    t.start()

class Test(unittest.TestCase):
    def test1(self):
        cursor = db.cursor()
        cursor.execute(QUERY_DEVICE_BY_ID, (1,))
        for (id, visited, status, shop_id, activated) in cursor:
            res = shop_id
            print('%s' % visited)
        cursor.close()

        self.assertEqual(res, 1)
    
    def test2(self):
        l1 = load_rd_devices()
        self.assertEqual(len(l1), 6)
    
    def test3(self):
        l2 = load_rd_shop()
        self.assertEqual(len(l2), 3)