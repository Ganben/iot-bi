# -*- coding: utf-8 -*-
# flask + vue + web for animation

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask import session
from flask import redirect
from flask import url_for

import redis
import logging
import datetime
import json
import os
import time
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__, static_url_path='/static')
app.secret_key = b'00010001c0febabec0febabe'
app.config.from_object(__name__)

rpool = redis.ConnectionPool(host='localhost', port=6379, db=0)
rd = redis.Redis(connection_pool=rpool)


logger = logging.getLogger('web-server')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh = logging.FileHandler('web-server.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

# enable CORS
CORS(app)


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/api/linchart', methods=['GET'])
def linchart():
    #
    bars = []
    xs = []
    td = datetime.date.today() - datetime.timedelta(days=6)
    for i in range(7):
        d = td + datetime.timedelta(days=i)
        xs.append(d.isoformat())
    d = rd.llen('aclist')
    
    d = 0 if d is None else d
    
    bars = [120, 20, 45, 120, 50, 61, d]
    ret = {
        "xs": xs,
        "serie": {
            'name': 'Activities',
            'type': 'bar',
            'data': bars
        }
    }

    return jsonify(ret)


#
@app.route('/api/status', methods=['GET'])
def all_status():
    #
    d = rd.lrange('devindex', 0, 100)
    keys = []
    for k in list(d):
        keys.append(k.decode('ascii'))
    # loop for retrieve all keys
    ret = []
    for k in keys:
        stsr = rd.get(k)
        if stsr is None:
            sts = { "status": [-1,-1,-1,-1],
            "counts": [0,0,0,0]}
        else:
            sts = json.loads(stsr.decode('ascii'))
        

        for i in range(2):
            if isinstance(sts['status'], list):
                #
                st = sts['status']
            else:
                st = [-1, -1, -1, -1]
            
            if isinstance(sts['counts'], list):
                ct = sts['counts']
            else:
                ct = [0,0,0,0]
            ret.append({
                "id": "%s%s" % (k,i+3),
                "st": st[i+2],
                "ct": ct[i+2]
            })
    return jsonify(ret)
    



    # loop to retrieve keys

    # return jsonify([
    #     {"id":"c1231", "st": 1, "ct": 0},
    #     {"id":"c1232", "st": 1, "ct": 0},
    #     {"id":"c1233", "st": 1, "ct": 120},
    #     {"id":"c1233", "st": 1, "ct": 155}
    # ])

@app.route('/api/logacts')
def all_logacts():
    #
    ret = []
    d = rd.lrange('aclist',0,100)
    for i in list(d):
        try:
            e = i.decode('ascii')
            logger.debug('logacts: %s' % e)
            ret.append(json.loads(e))
        except:
            logger.error('parse rd el error')

    return jsonify(ret)     
    # return jsonify([
    #     {"time":"11:10:11", "di": "12341234"},
    #     {"time":"11:10:11", "di": "12341234"},
    #     {"time":"11:10:11", "di": "12341234"},
    #     {"time":"11:10:11", "di": "12341234"},
    #     {"time":"11:10:11", "di": "12341234"},
    #     {"time":"11:10:11", "di": "12341234"}
    # ])

@app.route('/api/login', methods=['POST'])
def handle_login():
    # parse incoming data
    pass

@app.route('/api/accinfo', methods=['GET'])
@authenticate_require
def account_info():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)