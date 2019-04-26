# -*- coding: utf-8 -*-
# flask + vue + web for animation

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask import session
from flask import redirect
from flask import url_for
from flask import abort
from flask import request
# auth decorator support
from functools import wraps
import jwt
# pyjwt
# flask-principle is another choice

import redis
import logging
import datetime
import json
import os
import time
import base64
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

def verify_hd(jwttk):
    # verify a jwt token
    user = None
    data = jwttk.decode('ascii', 'ignore')
    # token = str.replace(str(data), 'Bearer ', '')
    token = jwttk.decode('ascii')
    logger.debug('%s' % jwttk.decode('ascii'))
    try:
        user = jwt.decode(token, app.config.get("SECRET_KEY"), algorithms=['HS256'])
    except Exception as e:
        logger.debug('jwt decode error %s' % e)
        return True
    return user

def basicauth(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not 'Authorization' in request.headers:
            abort(401)
        hd = request.headers.get('Authorization').encode('ascii', 'ignore')
        try:
            logger.debug('basic: %s' %  hd)
        except:
            pass
        # accept token auth
        #
                 
        if hd == b'Basic Z3Vlc3Q6Z3Vlc3Q=':
            logger.debug('basic auth equals')
            user = 'guest'
            return f(user, *args, **kws)
        elif str(hd).startswith('Bearer ') and verify_hd(hd[7::]):
            user = 'guest'
            return f(user, *args, **kws)
        else:
            abort(401)
    return decorated_function


def sessionauth(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'username' not in session:
            logger.debug('session denied')
            abort(401)
        return f(session['username'], *args, **kws)
    return decorated_function

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not 'Authorization' in request.headers:
            abort(401)
        
        user = None
        data = request.headers['Authorization'].encode('ascii', 'ignore')
        token = str.replace(str(data), 'Bearer ', '')
        try:
            user = jwt.decode(token, app.config.get("SECRET_KEY"), algorithms=['HS256'])
        except:
            abort(401)
        
        return f(user, *args, **kws)
    return decorated_function
### use for:
'''
axios({ method: 'POST', url: 'you http api here', headers: {Authorization: localStorage.token}, data: { user: 'name' } })
'''


# sanity check route
@app.route('/ping', methods=['GET', 'POST'])
@sessionauth
def ping_pong(user):
    data = json.loads(request.data)
    return jsonify(user)

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
@basicauth
def all_status(user):
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
@basicauth
def all_logacts(user):
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

def validate_login(post_dict):
    return True

@app.route('/api/login', methods=['POST'])
def handle_login():
    # parse incoming data
    pass
    # TODO process
    # user name, , serial no, OTP
    #
    logger.debug('post:%s' % request.get_json())
    post_json = request.get_json()

    if validate_login(post_json):

        # 
        #TODO retrieve user
        user_id = 'test'    
    else:
        abort(401)
    
    if True:
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e


@app.route('/api/accinfo', methods=['GET'])
@authorize
def account_info(user):
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)