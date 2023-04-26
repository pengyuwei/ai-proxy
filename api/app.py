#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coding=utf8

import pdb
import traceback
import time
import datetime
import os
import sys
import logging
import getopt
import requests
import json
from hashlib import md5
import redis
import toydb
from cache import Cache
from flask import jsonify

MSG_AUTH_FAILED = 'Invalid token, please relogin.'
CODE_SUCCESS = 0
CODE_AUTH_FAILED = 1
CODE_REQ_FAILED = 2
HTTP_REQUEST_SUCCESS = 200
HTTP_REQUEST_FAILED = 400
HTTP_UNAUTHORIZED = 401

debug_mode = False
config = None
CACHE_TIME = 30*24*60*60
is_daemon = False
port = 9090 # debug mode port
rank = {} # 排行榜
weekrank = {} # 周排行榜
remake_cache = False

def load_config():
    global config
    if config is None:
        with open('/etc/enapp.conf') as json_file:
            config = json.load(json_file)
    return config


def init(appname="ai"):
    global is_daemon, port, remake_cache
    is_daemon = False
    port = 9090
    opts, args = getopt.getopt(sys.argv[1:], "rdp:")
    for op, value in opts:
        if op == "-d":
            is_daemon = True
        elif op == "-p":
            port = int(value)
        elif op == '-r':
            remake_cache = True

    load_config()
    logging.basicConfig(
        level=config['log']['level'],
        format='%(asctime)s %(filename)s'
                '[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='%s_%d.log' % (appname, port),
        filemode='w')
    console = logging.StreamHandler()
    # INFO=20
    # DEBUG=10
    console.setLevel(config['log']['level'])
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    # logging.error("exception ", exc_info=1) # for traceback.print_exc()

    toydb.config = config
    Cache.HOST = config['cache']['host']
    Cache.PORT = config['cache']['port']


def log(self, *args):
    try:
        logging.debug(*args)
    except Exception as e:
        traceback.print_exc()
        print(repr(e))


def get_conn():
    db = toydb.ToyDB()
    db.connect(
        config['db']['user'],
        config['db']['password'],
        config['db']['host'],
        config['db']['db'],
        config['db']['port'])
    return db


def mysql_conn(f):
    def wrapper(*args):
        conn = get_conn()
        ret = f(*args, conn=conn)
        conn.close()
        return ret
    return wrapper


class http_method():
    @staticmethod
    def get(url, json_header=None, json_params=None, json_data=None):
        ret = None
        try:
            r = requests.get(url, headers=json_header, params=json_params, data=json_data)
            ret = r.text
        except:
            traceback.print_exc()
            logging.debug(traceback.format_exc())
        return ret


def daemonize():
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
    os.setsid()
    os.umask(0)


def closestd():
    sys.stdout.flush()
    sys.stderr.flush()
    si = open("/dev/null", 'r')
    so = open("/dev/null", 'a+')
    se = open("/dev/null", 'ab+', 0) # in python3 close buffer only use in bin mode
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


# token with user_id
def parse_request(req):
    ret = None
    token = req.headers.get('Authorization', None)
    if token is None:
        ret =  jsonify({'code': 1, 'message': MSG_AUTH_FAILED}), HTTP_UNAUTHORIZED
        return token, None, ret

    user_id = get_user_from_token(token)  # uid is int, user_id is unicode str
    if user_id is None:
        ret = jsonify({'code': 1, 'message': MSG_AUTH_FAILED}), HTTP_UNAUTHORIZED

    return token, user_id, ret

def get_today_str():
    return datetime.datetime.now().strftime("%Y%m%d")

def get_content(filename):
    with open(filename, 'r') as f:
        return f.read()