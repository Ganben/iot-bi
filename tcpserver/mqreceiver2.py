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
import pickle

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

class ShopLiveChart:
    shop_ids = {}

class DeviceLiveChart:
    device_ids = {}

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
            pin_id = int(device_id[0], 16)
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

            body = generate_chart_data(shopid)
            logger.info('web %s join in' % shopid)
            client.publish("shop%s" % shopid, body, qos=2)
        else:
            return

    else:
        logger.info('receive %s : %s' %(msg.topic, msg.payload))

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
    
    c.loop_forever()