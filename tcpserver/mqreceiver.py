# -*- coding: utf-8 -*-
# for receive the iot remote unit
# ganben

# mysql 
# mem data structure



import sys
import struct
import json

from paho.mqtt import client
import mysql.connector 

### MYSQL/DATAMODEL part
db = mysql.connector.connect(
    user='root',
    password = '123456',
    host = '127.0.0.1',
    database = 'iotbt'
)


class Queries:
    # query the devicedatalive
    query_device = ("SELECT id, visited, device_id, shop_id FROM stats_devicedatalive WHERE device_id = %s LIMIT 1") 
    # query the shopdatalive
    query_shop = ("SELECT id, visited, shop_id FROM stats_shopdatalive WHERE shop_id = %s LIMIT 1")
    # update the devicedatalive
    update_device = ("UPDATE stats_devicedatalive SET visited = %s WHERE device_id = %s")
    # update the shopdatalive
    update_shop = ("UPDATE stats_shopdatalive SET visited = %s WHERE shop_id = %s")

class DeltaVisited:
    # structure for accumulated things, limited for update frequency(or cache)
    map_store = {}
    dev_store = {}
    shop_store = {}
    # TODO: no limiter yet
    def put_dev(self, k, v):
        # k: device id
        # v: added count
        # get dev save query from cache
        if not self.dev_store.get(k, False):
            # query
            id, visited, device_id, shop_id = query_device(k, v)
            self.map_store[k] = shop_id
            self.dev_store[k] = visited
        else:
            shop_id = self.map_store.get(k)
            self.dev_store[k] += v
        return shop_id

    def put_shop(self, k, v):
        #k: shop id
        #v: change
        if not self.shop_store.get(k, False):
            id, visited = query_shop(k)
            self.shop_store[k] = visited
        else:
            self.shop_store[k] += v
    
    def update(self, k):
        # update dev and shop
        s = self.map_store.get(k)
        dv = self.dev_store.get(k)
        sv = self.shop_store.get(k)
        update_dev(k, dv)
        update_shop(k, sv)
        print("--update db--")
        update_commit()

deltaChange = DeltaVisited()

def update_commit():
    db.commit()

def update_dev(did, amount):
    # update
    cr = db.cursor(buffered=True)
    cr.execute(Queries.update_device % (did, amount))
    # cr.close()
    db.commit()

def update_shop(shid, amount):
    # update
    cr = db.cursor(buffered=True)
    cr.execute(Queries.update_shop % (shid, amount))
    # cr.close()
    db.commit()

def query_shop(shid, count = 1):
    cr = db.cursor(buffered=True)
    cr.execute(Queries.query_shop % (shid))
    for (id, visited, shop_id) in cr:
        visited += count
        break
    cr.close()
    return id, visited

def query_device(dvid, count=1):
    #device id, added counts
    cursorA = db.cursor(buffered=True)
    # cursorB = db.cursor(buffered=True)

    # query for shop id
    cursorA.execute(Queries.query_device % (dvid))
    # get 
    for (id, visited, device_id, shop_id) in cursorA:
        pass
        visited += count
        break
    cursorA.close()
    return id, visited, device_id, shop_id

def generate_chart_data(device_id):
    # body is a json fied
    shop_id = deltaChange.map_store.get(device_id)
    amount = deltaChange.shop_store.get(shop_id)
    # FD required shop visits update:
    return json.dumps({
        'label': '%s' % shop_id,
        'data': amount        
    })

### MQTT PART
# def connect to local web mqtt
def on_connect(client, userdata, flag_dict, rc):
    #
    print("connected with result code: %s" % str(rc))
    client.subscribe("dev")

def on_message(client, userdata, msg):
    #
    print("----receiv----")
    print("%s:%s" % (msg.topic, msg.payload))
    device_id, add = struct.unpack("QI", msg.payload)
    # start show case
    shopid = deltaChange.put_dev(device_id, add)
    deltaChange.put_shop(shopid, add)
    deltaChange.update(device_id)
    body = generate_chart_data(device_id)
    client.publish("shop%s" % shopid, body, qos=2)
    print('sent updated shop %s' % shopid)

c = client.Client(transport="websockets", client_id="receiver")
c.on_connect = on_connect
c.on_message = on_message
c.username_pw_set("guest", "guest")
c.ws_set_options(path="/ws")
c.connect("127.0.0.1", 15675, 60)


if __name__ == "__main__":
    
    c.loop_forever()