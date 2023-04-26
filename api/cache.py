#!/usr/bin/env python
# coding=utf8


import redis


class Cache:
    DELAULT_EXPIRE = 60 * 60 * 24
    LONG_EXPIRE = 60 * 60 * 24 * 7
    HOST = 'localhost'
    PORT = 6379
    
    @staticmethod
    def get_cache():
        return redis.Redis(host=Cache.HOST, port=Cache.PORT, decode_responses=True)
