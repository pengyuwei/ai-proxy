#!/usr/bin python
# -*- coding: UTF-8 -*-
# coding=utf8

from flask import Flask, jsonify, abort, make_response
from flask import Blueprint, render_template, session,abort
from flask import request, url_for
from flask_cors import CORS
from gevent import pywsgi

import app

webmain = Flask(__name__)
# support cross-origin
CORS(webmain, resources=r'/*', supports_credentials=True)
webapp = Blueprint('main', __name__)
CORS(webapp, resources=r'/*', supports_credentials=True)

from mod.api import webapp as webapi

if __name__ == '__main__':
    webmain.register_blueprint(webapi)

    app.init()

    if app.is_daemon:
        app.daemonize()
        app.save_pid()

    print("AI-API V1.0: %d\n" % app.port)

    if app.is_daemon:
        # production mode: use WSGI server
        app.closestd()
        # https product mode:
        server = pywsgi.WSGIServer(('0.0.0.0', app.port), webmain, 
                                   keyfile=app.config['api']['key'],
                                   certfile=app.config['api']['pem'])
        server.serve_forever()
    else:
        # https debug mode:
        app.debug_mode = True
        webmain.run(debug=True, host="0.0.0.0", port=app.port,
            ssl_context=(app.config['api']['pem'], app.config['api']['key']))
