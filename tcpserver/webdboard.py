# -*- coding: utf-8 -*-
# flask + vue + web for animation

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask import session
from flask import redirect
from flask import url_for

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


#
@app.route('/api/status', methods=['GET'])
def all_status():
    #
    return jsonify([
        {"id":"c1231", "st": 1, "ct": 0},
        {"id":"c1232", "st": 1, "ct": 0},
        {"id":"c1233", "st": 1, "ct": 120},
        {"id":"c1233", "st": 1, "ct": 155}
    ])

@app.route('/api/logacts')
def all_logacts():
    #
    return jsonify([
        {"time":"11:10:11", "di": "12341234"},
        {"time":"11:10:11", "di": "12341234"},
        {"time":"11:10:11", "di": "12341234"},
        {"time":"11:10:11", "di": "12341234"},
        {"time":"11:10:11", "di": "12341234"},
        {"time":"11:10:11", "di": "12341234"}
    ])

if __name__ == '__main__':
    app.run(host='localhost', port=5000)