# -*- coding:utf-8 -*-
# @Time: 2021/1/25 14:14
# @Author: Chenyang
# @File: mysql.py
# @Email: sygysut@163.com
# @Direction:

import pymysql
import traceback

from cy.tools.utils.get_config import handle_config


mysql_config = handle_config("database").get_section("mysql")


class Mysql(object):
    def __init__(self, host=mysql_config.get("host", "localhost") , port=mysql_config.get("port", 3306), \
                 user=mysql_config.get("user", "admin"), passwd=mysql_config.get("passwd", "admin"), \
                 db=mysql_config.get("database", "test")):
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        self.cursor = self.conn.cursor()

    def execute(self, sql, params=None, step=5000):
        """
        Execute your sql.
        :param sql: String for sql command without query.
        :param params: Batch command parameter, a list of data that is tuples.
        :return:
        """
        try:
            if params:
                length = len(params)
                for i in range(0, length, step):
                    self.cursor.executemany(sql, params[i:i + step if i + step < length else length])
                    self.conn.commit()
            else:
                self.cursor.execute(sql)
                self.conn.commit()
        except:
            print("Handle mysql error, exception is --> {} , sql is --> {}".format(traceback.format_exc(), sql))
            self.conn.rollback()

    def query(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor
        except:
            print("Query exception is --> {}".format(traceback.format_exc()))

    def close(self):
        try:
            self.conn.close()
            return True
        except:
            print("Close failure, is --> {}".format(traceback.format_exc()))

