#!/usr/bin/env python
# coding=utf8

# Create time:2017-5-4
# Update time:2017-5-4
# Version: 1
# sudo apt-get install python-mysqldb

import MySQLdb
import sys
from importlib import reload

# reload(sys)
# sys.setdefaultencoding('utf8')
config = None

class ToyDB:
    conn = None
    cur = None

    @staticmethod
    def get_conn():
        db = ToyDB()
        db.connect(
            config['db']['user'],
            config['db']['password'],
            config['db']['host'],
            config['db']['db'],
            config['db']['port'])
        return db

    def connect(self, user, passwd, ip, db, port=3306):
        self.conn = MySQLdb.connect(
            host=ip, port=port,
            user=user, passwd=passwd,
            db=db, charset="utf8")
        self.cur = self.conn.cursor()
        self.cur.execute("SET NAMES utf8mb4;")
        self.conn.commit()

    def run_sql(self, sql):
        self.cur.execute(sql)
        self.conn.commit()
        print(self.conn.insert_id())
        return self.cur.lastrowid

    def select_sql(self, sql):
        aa = self.cur.execute(sql)
        ret = self.cur.fetchmany(aa)
        return ret
    
    def effect_rows(self):
        return self.cur.rowcount

    def close(self):
        self.cur.close()
        self.conn.close()

    def openid_to_userid(self, openid):
        user_id = None
        sql = 'SELECT id FROM ENApp.users ' \
            'where wxopenid="%s" limit 1;' % (openid)
        rs = self.select_sql(sql)
        if len(rs) > 0:
            user_id = rs[0][0]
        return user_id
