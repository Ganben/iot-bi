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

import datetime
import pickle
import enum

import pygtrie
from anytree import Node, RenderTree

import redis
from paho.mqtt import client
import mysql.connector 

### set up logging
logger = logging.getLogger('mqwatcher')
logger.setLevel(logging.DEBUG)

# fh
fh = logging.FileHandler('mqwathcer.log')
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
    
    def put_heartbeat(self, hb):
        # put heartbeat to rd
        self.rd.rpush('hblist', hb)

    def put_activity(self, action):
        # put activity to
        self.rd.rpush('aclist', action)
    
    def dayswap(self):
        # swap cached msgs
        while self.rd.llen('hblist') > 0:
            o = self.rd.lpop('hblist')
            # do something

        while self.rd.llen('aclist') > 0:
            o = self.rd.lpop('aclist')
            # do something

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
    reto = MsgDev(str_content)
    return 

def parseID(str_content):
    # parse the str to
    ss = str_content.split('.')
    reto = MsgRemote(str_content)
    return

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
    elif msg.topic == 'remote':
        r = parseID(msg.payload.decode('ascii'))


def init():
    pass


if __name__ == "__main__":
    init()
    c = client.Client(client_id="receiver")
    c.on_connect = on_connect
    c.on_message = on_message
    c.username_pw_set("guest", "guest")
    c.ws_set_option(path="/")
    c.connect("127.0.0.1", 1883, 60)
    c.loop_forever()