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

def send_bh():
    publish.single("remote", "hb.ecfabc9c3610.1.1100", hostname="aishe.org.cn", port=1883)

def send_dv():
    publish.single("dev", "ecfabc9c3610.4.110", hostname="aishe.org.cn", port=1883)


if __name__ == "__main__":
    # read sys.argv[1]: id, [2] count
    if len(sys.argv) < 3:
        raise Exception('require device and counts')
    # pl = struct.pack("", int(sys.argv[1]), int(sys.argv[2]))
    # pl = "%2d%2d%2d%2d" % (int(sys.argv[1]), 0, int(sys.argv[2]), 0)
    # real wlan addr: 192.168.31.122
    ho = sys.argv[2]
    # assert(ho, str)
    # pl = f"{int(sys.argv[1]):x}"
    pl = "%s.%s" % (sys.argv[1], 4)
    publish.single("dev", pl, hostname=ho, port=9883, transport="websockets", retain=False, qos=2)
    print("--sent--")