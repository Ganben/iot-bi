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

import redis
from paho.mqtt import client
import mysql.connector 

### set up logging
logger = logging.getLogger('mqreceiver')
logger.setLevel(logging.DEBUG)

# fh
fh = logging.FileHandler('mqreceiver.log')
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
# rd.set_response_callback('HGET', int)
class Queries:
    # query the devicedatalive
    query_device = ("SELECT id, visited, device_id, shop_id FROM stats_devicedatalive WHERE device_id = %s LIMIT 1;") 
    # query the shopdatalive
    query_shop = ("SELECT id, visited, shop_id FROM stats_shopdatalive WHERE shop_id = %s LIMIT 1;")
    # update the devicedatalive
    update_device = ("UPDATE stats_devicedatalive SET visited = %s WHERE device_id = %s ;")
    # update the shopdatalive
    update_shop = ("UPDATE stats_shopdatalive SET visited = %s WHERE shop_id = %s ;")

class DeltaVisited:
    # structure for accumulated things, limited for update frequency(or cache)
    map_store = {}
    dev_store = {}
    shop_store = {}
    # rdb = rd
    # TODO: no limiter yet
    def __init__(self, rdb):
        self.rdb = rdb

    def put_dev(self, k, v):
        # k: device id
        # v: added count
        # get dev save query from cache
        shop_id = 0
        if self.dev_store.get(k, False):
            # query
            logger.info('found existing dev id %s' % k)
            id, visited, device_id, shop_id = query_device(k, v)
            if not id:
                # not save knonw id
                logger.debug('unknow dev id')
                return 0
            # self.map_store[k] = shop_id
            visited = self.dev_store[k] + 1
            self.dev_store[k] = visited
            self.rdb.set(k, visited)

        else:
            logger.info('put new dev id %s' % k)
            # fetch new stuff from sql db
            id, visited, device_id, shop_id = query_device(k, v)
            if not id:
                logger.debug('unknow new dev id')
                return 0
            # not saving unknow id
            self.map_store[k] = shop_id
            self.dev_store[k] = visited + v
            self.dev_store[k] = v + self.dev_store.get(k, 0)
            self.rdb.set(k, self.dev_store[k])

        return shop_id

    def put_shop(self, k, v):
        #k: shop id
        #v: change
        if not k:
            logger.error('shop id None')
            return False

        if not self.shop_store.get(k, False):
            id, visited = query_shop(k)
            self.shop_store[k] = visited
        else:
            self.shop_store[k] += v
    
    def update(self, k):
        # update dev and shop
        s = self.map_store.get(k)
        dv = self.dev_store.get(k)
        sv = self.shop_store.get(s)
        update_dev(k, dv)
        update_shop(s, sv)
        logger.info("--update db--")
        update_commit()

deltaChange = DeltaVisited(rd)

def update_commit():
    logger.debug('db commit')
    db.commit()

def update_dev(did, amount):
    logger.debug('upt device %s' % did)
    # update
    rd.set(did, amount)
    cr = db.cursor(buffered=True)
    try:
        r = cr.execute(Queries.update_device % (did, amount))

        logger.debug('db dev update res: %s' % r)
    except Exception as e:
        logger.error('db sql error:%s' % e)
    finally:
        cr.close()
        db.commit()
    # cr.close()

def update_shop(shid, amount):
    logger.debug('upt shop %s' % shid)
    if not shid:
        return False

    # update
    cr = db.cursor(buffered=True)
    r = cr.execute(Queries.update_shop % (shid, amount))
    cr.close()
    logger.debug('db shop update %s' % r)
    db.commit()
    # cr.close()

def query_shop(shid, count = 1):
    logger.debug('query shop %s' % shid)
    cr = db.cursor(buffered=True)
    try:
        cr.execute(Queries.query_shop % (shid))
    except Exception as e:
        logger.debug('%s' % e)
        return 0, 0
    id = 0
    visited = 0
    shop_id = 0
    for (id, visited, shop_id) in cr:
        visited += count
        break
    cr.close()
    if shop_id == 0 and id == 0:
        visited = 1
    logger.info("qr shop: %s visited" % visited)
    return id, visited

def query_device(dvid, count=1):
    logger.debug('qr devi %s' % dvid)
    #device id, added counts
    cursorA = db.cursor(buffered=True)
    # cursorB = db.cursor(buffered=True)


    # query for shop id
    try:
        cursorA.execute(Queries.query_device % (dvid))
    except Exception as e:
        logger.debug('%s' % e)
        return 0, 0, 0, 0
    
    id = 0
    visited = 0
    device_id = 0
    shop_id = 0
    
    # get 
    for (id, visited, device_id, shop_id) in cursorA:
        pass
        visited += count
        logger.info('fetch result: %s' % visited)
        break
    
    cursorA.close()
    # make sure the unknow will not save TODO
    logger.debug('determin sql or redis')

    if id == 0 and rd.get(dvid):
        try:
            visited = int(rd.get(dvid)) 
            visited += count
            rd.set(dvid, visited)
        except Exception as e:
            logger.error('redis not found')
        
    
    logger.info("dev: %s visited" % visited)
    return id, visited, device_id, shop_id

def generate_chart_data(device_id):
    # body is a json fied
    shop_id = deltaChange.map_store.get(device_id)
    amount = deltaChange.dev_store.get(device_id)
    # FD required shop visits update:
    return json.dumps({
        'label': '%s' % device_id,
        'data': amount        
    })

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
        add = 1
        try:
            # device_id = struct.unpack("32s", msg.payload)
            # device_id_hex = ## modified from last change, hex string to int
            device_id = int(msg.payload, 16)
            # add = 1
            # device_id, add = struct.unpack("QI", msg.payload)
            # device_id = int(msg.payload[0])
            logger.info("did:%d" % device_id)
        except:
            device_id = 1
            logger.error('unpack error')
        
        
        if not device_id == 0:
            # add = int(msg.payload[2])
            shopid = deltaChange.put_dev(device_id, add)
            logger.info('put shop %s' % shopid)
            deltaChange.put_shop(shopid, add)
            deltaChange.update(device_id)
            body = generate_chart_data(device_id)

        try:
            client.publish("shop%s" % shopid, body, qos=2)
            logger.info('sent updated shop %s' % shopid)
        except:
            logger.error('update error')
        # start show case
    else:
        logger.info('receive %s : %s' %(msg.topic, msg.payload))

# c = client.Client(transport="websockets", client_id="receiver")
c = client.Client(client_id="receiver")
c.on_connect = on_connect
c.on_message = on_message
c.username_pw_set("guest", "guest")
c.ws_set_options(path="/")
c.connect("127.0.0.1", 1883, 60)


if __name__ == "__main__":
    
    c.loop_forever()