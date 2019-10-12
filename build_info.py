# coding: utf-8
"""
获取楼盘详细信息
"""
import urllib2
import types
import psycopg2.extras
import psycopg2 as pg
from bs4 import BeautifulSoup
from siemtools import utils
from config import *

LOGGER = utils.initLogger(LOG_ROUTE)


def build_info(url_list, batch_id):
    """
    获取楼盘详细信息
    :param url_list: 楼盘链接URL
    :return:
    """
    dict_list = []
    try:
        for i in range(len(url_list)):
            html_dict = {}
            type_list = []
            data_list = []
            html = urllib2.urlopen(url_list[i]).read()
            soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            for msg_d in soup.find_all("div", class_="name"):
                type_list.append(msg_d.text)
            for msg_d in soup.find_all("div", class_="des"):
                data_list.append(msg_d.text.strip().replace(" ", ""))
            print data_list, type_list
            for i in range(len(type_list)):
                if type_list[i] in BUILD_INFO_DICT.keys():
                    html_dict[BUILD_INFO_DICT[type_list[i]]] = data_list[i].\
                        replace("\n", " ").replace(u"[查看详情]", "").replace(u"[价格走势]", "").\
                        replace(u"[查看地图]", "").replace(u"[房贷计算器]", "")
                html_dict["batch_id"] = batch_id
            dict_list.append(html_dict)
            print len(dict_list), dict_list
            data_list = []
            type_list = []
            print data_list, type_list
        return dict_list
    except Exception, ex:
        LOGGER.error("build_info get failed,msg{0:s}".format(str(ex)))
        # raise Exception(str(ex))


def ajk_data_sql(table_name, data_d):
    """
    拼接SQL语句
    :param table_name: 插入目的数据表表名
    :param data_d: 要插入的数据
    :return:
    """
    sql_str = "insert into {0:s}(".format(table_name)
    key_str = ""
    value_str = ""
    for key in data_d:
        key_str = key_str + key + ","
        if type(data_d[key]) in [types.IntType, types.BooleanType]:
            value_str = value_str + str(data_d[key]) + ","
        elif type(data_d[key]) in [types.StringType, types.UnicodeType]:
            value_str = value_str + "'" + data_d[key] + "',"
    print sql_str + key_str[:-1] + ") values (" + value_str[:-1] + ");"
    return sql_str + key_str[:-1] + ") values (" + value_str[:-1] + ");"


def ajk_data_insert(table_name,
                    data_dict,
                    host="192.168.159.128",
                    port=5432,
                    user="postgres",
                    password="postgres",
                    dbname="ajk_data"):
    """
    向数据库中插入数楼盘信息数据
    :param host: 数据库地址
    :param port: 数据库端口号
    :param user: 用户名
    :param password: 密码
    :param dbname: 数据库名称
    :param table_name: 数据表名称
    :param data_dict: 要插入的数据
    :return:
    """
    try:
        conn = pg.connect(host=host,
                          port=port,
                          user=user,
                          password=password,
                          dbname=dbname)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        for i in range(len(data_dict)):
            cur.execute(ajk_data_sql(table_name, data_dict[i]))
        conn.commit()
        return True
    except Exception, ex:
        LOGGER.error("ajk_data insert failed,msg{0:s}".format(str(ex)))
        # raise Exception(str(ex))

# d = [u'https://heb.fang.anjuke.com/loupan/canshu-411852.html', u'https://heb.fang.anjuke.com/loupan/canshu-412237.html', u'https://heb.fang.anjuke.com/loupan/canshu-430815.html', u'https://heb.fang.anjuke.com/loupan/canshu-253948.html', u'https://heb.fang.anjuke.com/loupan/canshu-417997.html', u'https://heb.fang.anjuke.com/loupan/canshu-253847.html', u'https://heb.fang.anjuke.com/loupan/canshu-411209.html', u'https://heb.fang.anjuke.com/loupan/canshu-418732.html', u'https://heb.fang.anjuke.com/loupan/canshu-417422.html', u'https://heb.fang.anjuke.com/loupan/canshu-253891.html', u'https://heb.fang.anjuke.com/loupan/canshu-428594.html', u'https://heb.fang.anjuke.com/loupan/canshu-253969.html', u'https://heb.fang.anjuke.com/loupan/canshu-412225.html', u'https://heb.fang.anjuke.com/loupan/canshu-253899.html', u'https://heb.fang.anjuke.com/loupan/canshu-413882.html']
# d_d = build_info(d)
# print d_d
# ajk_data_insert("b", d_d)
