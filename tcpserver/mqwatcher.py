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

import pygtrie

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

### db part


### shop chart live part


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