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
logger = logging.getLogger('mqreceiver2')
logger.setLevel(logging.DEBUG)

# fh
fh = logging.FileHandler('mqreceiver2.log')
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
# db = mysql.connector.connect(
#     user='root',
#     password = '123456',
#     host = '127.0.0.1',
#     database = 'iotbt',
#     charset = 'utf8mb4'
# )

# rd = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
rpool = redis.ConnectionPool(host='localhost', port=6379, db=0)
rd = redis.Redis(connection_pool=rpool)


# def generate_chart_data(device_id):
#     # body is a json fied
#     shop_id = deltaChange.map_store.get(device_id)
#     amount = deltaChange.dev_store.get(device_id)
#     # FD required shop visits update:
#     return json.dumps({
#         'label': '%s' % device_id,
#         'data': amount        
#     })

## DATAMODEL Part
# map of device id and shop id, read from redis--modeled in mysql interface
class DevShopMap:
#    device_id = []
    shop_ids = {}
dsMap = pygtrie.CharTrie()

class ShopDevMap:
    device_ids = {}

sdMap = pygtrie.CharTrie()

class ShopLiveChart:
    shop_ids = {}  # should be pygtrie for prefix advantage
    def gen(self, shopid):
        return {
        'id': shopid,
        'labels': [
            1,
            2,
            3
        ],
        'data': [
            3,
            4,
            5
        ],
        'status': [
            'E',
            'N',
            'E'
        ]
        }
liveShopChart = pygtrie.CharTrie()

class DeviceLiveChart:
    device_ids = {}
    def gen(self, label):
        return {
        'label':label,
        'names': [
            "product1",
            "product2",
            "product3",
            "product4"
        ],
        'stats':[
            4,
            5,
            6,
            7
        ],
        'status': [
            1,
            0,
            0,
            1
        ]
        }
liveDeviceChart = pygtrie.CharTrie()

# init with sample data
def init_data():
    # fill all trie with specified data
    dsMap['1'] = 1
    dsMap['2'] = 1
    dsMap['3'] = 1
    dsMap['4'] = 2
    dsMap['5'] = 2
    dsMap['6'] = 3
    sdMap['1'] = [1,2,3]
    sdMap['2'] = [4,5]
    sdMap['3'] = [6]
    shoplive = ShopLiveChart()
    devicelive = DeviceLiveChart()
    for i in [1,2,3,4,5,6]:
        liveDeviceChart[str(i)] = devicelive.gen(i)

    for i in [1,2,3]:
        liveShopChart[str(i)] = shoplive.gen(i)

def load_data():
    # key 1
    key_ldc = 'livedevicechart'
    key_lsc = 'liveshopchart'
    key_sdm = 'sdMap'
    key_dsm = 'dsMap'
    if rd.exists(key_dsm):
        dsMap = pickle.loads(rd.get(key_dsm))
    else:
        pass
    
    if rd.exists(key_sdm):
        sdMap = pickle.loads(rd.get(key_sdm))
    else:
        pass

    if rd.exists(key_ldc):
        liveDeviceChart = pickle.loads(rd.get(key_ldc))
    else:
        pass

    if rd.exists(key_lsc):
        liveShopChart = pickle.loads(rd.get(key_lsc))
    else:
        pass
    

### MQTT PART
# def connect to local web mqtt
def on_connect(client, userdata, flag_dict, rc):
    #
    logger.info("connected with result code: %s" % str(rc))
    client.subscribe("dev")
    client.subscribe("remote")
def on_message(client, userdata, msg):
    #
    logger.debug("----receiv----")
    logger.debug("%s:%s" % (msg.topic, msg.payload))
    if msg.topic == "dev":
        
        try:
            # device_id = struct.unpack("32s", msg.payload)
            # device_id_hex = ## modified from last change, hex string to int
            dev_str = msg.payload.decode('ascii').split('.')
            
            device_id = int(dev_str[0], 16)
            pin_id = int(dev_str[0], 16)
            logger.info("dev_s:%s" % dev_str)

        except:
            # device_id = 1
            logger.error('unpack error')
            return
        
        try:
            device_id = int(dev_str[0], 16) #parse hex to int
            device_pin = int(dev_str[1])
        except:
            logger.error('wrong device id format')
            return

        
        
        # if not device_id == 0:
            # add = int(msg.payload[2])
            # shopid = deltaChange.put_dev(device_id, 1)
            # logger.info('put shop %s' % shopid)
            # deltaChange.put_shop(shopid, 1)
            # deltaChange.update(device_id)
            # body = generate_chart_data(device_id)

        try:
            client.publish("shop%s" % shopid, body, qos=2)
            logger.info('sent updated shop %s' % shopid)
        except:
            logger.error('update error')
        # start show case
    elif msg.topic == 'remote':
        logger.info('receive %s : %s' %(msg.topic, msg.payload))
        remote_register = str(msg.payload.decode('ascii')).split('.')
        if len(remote_register) == 4 and remote_register[0] == 'hb':
            #TODO: push the device's online duration
            #device_id = int(remote_register[1], 16)
            #time = int(remote_register[2]) # right now worked
            try:
                logger.debug('remote/hb/device:%s' % int(remote_register[1], 16))
            except:
                logger.error('hb parse error:%s' % remote_register)
            device_id = int(remote_register[1], 16)
            time = int(remote_register[2]) # in munite
            live_status = parseSigStatus(remote_register[3]) # TODO: need filter
        
        elif len(remote_register) == 3 and remote_register[0] =='hb':
            #backward compatible
            device_id = int(remote_register[1], 16)
            time = int(remote_register[2])
            
        
        elif len(remote_register) == 3 and remote_register[0] == 'wb':
            #new_device_id = int(remote_register[0], 16)
            websession = remote_register[2]
            # need shopid from the msg
            shopid = int(remote_register[1])

            body = generate_shopchart_data(shopid)
            logger.info('web %s join in' % shopid)
            client.publish("shop%s" % shopid, body, qos=2)
        else:
            return

    else:
        logger.info('receive %s : %s' %(msg.topic, msg.payload))

def generate_shopchart_data(shopid):
    
    d = liveShopChart.get(str(shopid))
    l = []
    for i in range(len(d['labels'])):
        l.append({
            'label':str(d['labels'][i]),
            'data': d['data'][i]
            })
    return json.dumps(l)


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

# c = client.Client(transport="websockets", client_id="receiver")
c = client.Client(client_id="receiver")
c.on_connect = on_connect
c.on_message = on_message
c.username_pw_set("guest", "guest")
c.ws_set_options(path="/")
c.connect("127.0.0.1", 1883, 60)


if __name__ == "__main__":
    init_data()
    c.loop_forever()


class Tests(unittest.TestCase):
    def test1(self):
        s1 = ShopLiveChart
        s1.shop_ids = {
            1:12,
            2:11,
            3:13
        }
        po = pickle.dumps(s1)
        rd.set('somekey', po)
        uo = pickle.loads(rd.get('somekey'))
        self.assertEqual(True, s1 == uo)