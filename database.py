# coding: utf-8
"""
数据库操作
"""
import psycopg2.extras
import psycopg2 as pg
from config import *
from siemtools import utils

LOGGER = utils.initLogger(LOG_ROUTE)


def db_table_drop(host="192.168.159.128",
                  port=5432,
                  user="postgres",
                  password="postgres",
                  dbname="ajk_data"):
    """
    删除数据表
    :param host: 数据库IP地址
    :param port: 数据库端口号
    :param user: 用户名
    :param password: 密码
    :param dbname: 数据库名称
    :return:
    """
    try:
        conn = pg.connect(host=host,
                          port=port,
                          user=user,
                          password=password,
                          dbname=dbname)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        for i in range(len(AJK_TABLE)):
            cur.execute("drop table {0:s};".format(AJK_TABLE[i]))
        conn.commit()
        return True
    except Exception, ex:
        LOGGER.error("Data base table drop failed,msg:{0:s}".format(str(ex)))
        raise Exception(str(ex))


def bd_table_clear(host="192.168.159.128",
                   port=5432,
                   user="postgres",
                   password="postgres",
                   dbname="ajk_data"):
    """
    清除表中数据
    :param host: 数据库IP地址
    :param port: 数据库端口号
    :param user: 用户名
    :param password: 密码
    :param dbname: 数据库名称
    :return:
    """
    try:
        conn = pg.connect(host=host,
                          port=port,
                          user=user,
                          password=password,
                          dbname=dbname)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        for i in range(len(AJK_TABLE)):
            cur.execute("delete from {0:s} where 1=1;".format(AJK_TABLE[i]))
        conn.commit()
        return True
    except Exception, ex:
        LOGGER.error("Table data clear failed,msg:{0：s}".format(str(ex)))
        raise Exception(str(ex))


def db_table_create(host="192.168.159.128",
                    port=5432,
                    user="postgres",
                    password="postgres",
                    dbname="ajk_data"):
    """
    创建数据表
    :param host: 数据库IP地址
    :param port: 数据库端口号
    :param user: 用户名
    :param password: 密码
    :param dbname: 数据库名
    :return:
    """
    try:
        conn = pg.connect(host=host,
                          port=port,
                          user=user,
                          password=password,
                          dbname=dbname)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        for i in range(len(AJK_TABLE_CREATE)):
            cur.execute("{0:s}".format(AJK_TABLE_CREATE[i]))
        conn.commit()
        return True
    except Exception, ex:
        LOGGER.error("Table create failed,msg:{0:s}".format(str(ex)))
        raise Exception(str(ex))
