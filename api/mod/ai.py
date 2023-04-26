#!/usr/bin python
# -*- coding: UTF-8 -*-
# coding=utf8

import sys 
sys.path.append("..") 
from cache import Cache

class AI:
    def _get_key(self, question):
        return "AI_Q_" + question

    def ask(self, question):
        """问题写入队列即返回，不等待回答"""
        c = Cache.get_cache(question)
        key = self._get_key(question)
        ans = c.set(key, None, ex=Cache.DELAULT_EXPIRE)
        return True

    def get_answer(self, question):
        c = Cache.get_cache(question)
        key = self._get_key(question)
        ans = c.get(key)
        return ans