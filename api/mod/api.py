#!/usr/bin python
# -*- coding: UTF-8 -*-
# coding=utf8

from flask import Flask, jsonify, abort, make_response
from flask import request, url_for
from flask_cors import CORS
from flask import Blueprint, render_template, session,abort

import sys 
sys.path.append("..") 
from mod.ai import AI
import logging
import app

webapp = Blueprint('ai', __name__)
CORS(webapp, resources=r'/*', supports_credentials=True)

MSG_NOAI = 'AI去休假了，晚点再来吧'
CODE_SUCCESS = 0
CODE_AUTH_FAILED = 1
CODE_REQ_FAILED = 2
HTTP_REQUEST_SUCCESS = 200
HTTP_REQUEST_FAILED = 400
HTTP_UNAUTHORIZED = 401


@webapp.route('/api/v1.0/ai/<string:question>', methods=['GET'])
def api_ai_get(question):
    token, user_id, ret = app.parse_request(request)
    if token is None or user_id is None:
        return ret

    logging.info("GET /ai %s, %s", user_id, question)
    ai = AI()
    rs = ai.get_answer(question)
    if rs is None:
        return jsonify({'code': 1, 'message': MSG_NOAI}), HTTP_REQUEST_FAILED

    ret = {"code": 0, "message": "请耐心等待AI理解后就会回答你"}
    return jsonify(ret), 200

# 1.向AI提问：提问时问题放入消息队列就返回
@webapp.route('/api/v1.0/ai/<string:question>', methods=['POST'])
def api_ai_ask(question):
    token, user_id, ret = app.parse_request(request)
    if token is None or user_id is None:
        return ret

    logging.info("POST /ai %s, %s", user_id, question)
    ai = AI()
    rs = ai.ask(question) # 问题写入队列即返回，不等待回答
    if rs is None:
        return jsonify({'code': 1, 'message': MSG_NOAI}), HTTP_REQUEST_FAILED

    ret = {"code": 0, "message": "请等待AI理解后就会回答你"}
    return jsonify(ret), 200