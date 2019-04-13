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
import unittest

import time
import datetime
import pickle
import enum

import pygtrie
from anytree import Node, RenderTree

import redis
from paho.mqtt import client
# import mysql.connector

### set up logging
logger = logging.getLogger('mqwatcher')
logger.setLevel(logging.DEBUG)

# fh
fh = logging.FileHandler('mqwatcher.log')
fh.setLevel(logging.DEBUG)
# ch
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

rpool = redis.ConnectionPool(host='localhost', port=6379, db=0)
rd = redis.Redis(connection_pool=rpool)

dsMap = pygtrie.CharTrie()

sdMap = pygtrie.CharTrie()
#use normal dict for node dict map

# no map required
# all put to a trie
# and use anytree to generate all cached stats, use render tree

class DeviceNode(Node):
    # all device node for status
    # maybe not required, just iter all dev in cache
    pass
    #TODO

### db part
class Rdb:
    def __init__(self):
        self.rd = rd
        self.dsMap = dsMap
        self.sdMap = sdMap
        self.devices = {}
        self.actions = {}
        self.hbs = {}
        if self.rd.get('date') is None:
            d = datetime.datetime.now().date()
            self.rd.set('date', d)
            self.date = d
        else:
            ds = self.rd.get('date').decode('ascii')
            dsl = ds.split('-')
            logger.debug('load time:%s' % ds)
            self.date = datetime.datetime(int(dsl[0]), int(dsl[1]), int(dsl[2]))
        # if self.rd.llen('hblist') > 0:
        # TODO: add cached reload
        while self.rd.llen('hblist') > 0:
            pass
        
        while self.rd.llen('aclist') > 0:
            pass

    
    def put_heartbeat(self, hb):
        # put heartbeat to rd
        self.rd.rpush('hblist', hb)

    def put_activity(self, action):
        # put activity to
        self.rd.rpush('aclist', action)
    
    def add_dev(self, lin):
        logger.warn('new dev:%s' % lin[0])
        self.devices[lin[0]] = {
            "time": 0,
            "status": [0,0,0,0]
        }
    
    def add_hb(self, lin):
        logger.debug('add hb:%s.%s.%s.%s' % (lin[0],lin[1],lin[2],lin[3]))
        self.devices[lin[1]] = {
            "time": 3*int(lin[2]),
            "status": parseSigStatus(lin[3])
        }
        # self.
        if datetime.datetime.today() - self.date >= datetime.timedelta(days=1):
            self.dayswap()
            self.reset()
            self.date = self.date + datetime.timedelta(days=1)
    
    def add_act(self, lin):
        #
        #
        if lin is None:
            return
        if not isinstance(lin, list):
            return
        if self.actions.get(lin[0]) is None:
            self.actions[lin[0]] = [0,0,0,0]
            self.actions[lin[0]][lin[1]-1] = 1
        else:
            stats = self.actions[lin[0]]
            # stats[0] = stats[0] + 1
            stats[lin[1]-1] = stats[lin[1]-1] + 1
        t = time.strftime('%H:%M:%S', time.localtime())
        action_item = json.dumps({
            "time": t,
            "devicepin": "%s%s" % (lin[0],lin[1]),
            "counts": stats[lin[1]-1]
        })
        self.rd.rpush('aclist', action_item)

    def dayswap(self):
        # swap cached msgs
        if self.rd.llen('hblist') > 0:
            o = self.rd.delete('hblist')
            # do something

        if self.rd.llen('aclist') > 0:
            o = self.rd.delete('aclist')
            # do something
        for key, _ in self.devices.items():
            # for i in range(4):
            self.rd.rpush('deviceslist', key)

        for key, value in self.actions.items():
            self.rd.rpush('actionlist', key)
            for i in range(len(value)):
                # put key+index to rd
                k = '%s%s' % (key, i)
                self.rd.set(k, value[i])
    
    def reset(self):
        self.devcies.clear()
        self.actions.clear()
        # self.rd.delete('deviceslist')

        
    def query_status(self, pin):
        # query id+pin
        if self.devices.get(pin) is None:
            return [0, 0, 0, 0]
        else:
            return self.devices.get(pin)
    
    def query_actions(self, pin):
        if self.actions.get(pin) is None:
            return [-1, -1, -1, -1]
        else:
            return self.actions.get(pin)

rdb = Rdb()

class ProxyState(enum.Enum):
    Heartbeat = 1
    Regist = 2
    Activity = 3

class MsgRemote:
    def __init__(self, content):
        self.content = content
        self.device = parseID(content)
        self.header = parseHeader(content)
    
    def push_to_db(self, db):
        #
        pass

class MsgDev:
    def __init__(self, content):
        self.content = content
        self.device = parseID(content)
        self.state = ProxyState.Activity

class Proxy:
    def __init__(self, subject):
        self._subject = subject
        self._proxystate = subject.state


class ProxyMsg(Proxy):
    def push(self):
        # push to db/other service depend on its proxy state
        if self._proxystate == ProxyState.Activity:
            #
            pass


### shop chart live part
def parseDev(str_content):
    #
    ss = str_content.split('.')
    if isinstance(ss, list):
        logger.debug("dev=%s" %(ss[0]))
    # reto = MsgDev(str_content)
    return ss

def parseID(str_content):
    # parse the str to
    ss = str_content.split('.')
    if isinstance(ss, list):
        logger.debug("dev=%s" % ss[0])
    # reto = MsgRemote(str_content)
    return ss

def parseSigStatus(s):
    if len(s) != 4:
        return [1,1,1,1]
    else:
        r = []
        for i in s:
            if i == '1':
                r.append(1)
            elif i == '0':
                r.append(0)
        return r

### MQTT part

def on_connect(client,userdata, flag_dict, rc):

    logger.info("connected with result: %s" % str(rc))
    client.subscribe("dev")
    client.subscribe("remote")

def on_message(client, userdata, msg):
    # use proxy mode to call update
    logger.debug("--incomming-msg--")
    logger.info("%s:%s" %(msg.topic, msg.payload))
    # selective with topic, then process payload
    if msg.topic == 'dev':

        r = parseDev(msg.payload.decode('ascii'))
        rdb.add_act(r)
        
    elif msg.topic == 'remote':
        r = parseID(msg.payload.decode('ascii'))
        try:
            b = msg.payload.decode('ascii').split('.')
            if len(b) == 1:
            # new registered device
                rdb.add_dev(b)
            else:
                rdb.add_hb(b)
        except:
            logger.error('remote parse error')

def init():
    pass

c = client.Client(client_id="watcher")
c.on_connect = on_connect
c.on_message = on_message
c.username_pw_set("guest", "guest")
# c.ws_set_option(path="/")
c.connect("127.0.0.1", 1883, 60)

if __name__ == "__main__":
    init()
    # c = client.Client(client_id="receiver")
    # c.on_connect = on_connect
    # c.on_message = on_message
    # c.username_pw_set("guest", "guest")
    # c.ws_set_option(path="/")
    # c.connect("127.0.0.1", 1883, 60)
    c.loop_forever()