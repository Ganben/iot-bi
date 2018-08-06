# -*- coding: utf-8 -*-
# for simulation of the iot remote unit
# ganben

import sys
import struct

from paho.mqtt import (
    client,
    publish,
)


# def connect to local web mqtt
def on_connect(client, userdata, flag_dict, rc):
    #
    print("connected with result code: %s" % str(rc))
    # client.subscribe("shop1")

def on_message(client, userdata, msg):
    #
    print("%s:%s" % (msg.topic, msg.payload))

c = client.Client(transport="websockets")
c.on_connect = on_connect
c.on_message = on_message
# c.ws_set_options(path="/ws")
# c.connect("127.0.0.1", 15675, 60)

# c.loop_forever()

if __name__ == "__main__":
    # read sys.argv[1]: id, [2] count
    if len(sys.argv) < 3:
        raise Exception('require device and counts')
    pl = struct.pack("QI", int(sys.argv[1]), int(sys.argv[2]))
    publish.single("dev", pl, hostname="127.0.0.1", port=9883, transport="websockets", retain=False, qos=2)
    print("--sent--")