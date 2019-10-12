# coding: utf-8
'''
获取安居客楼盘评测
'''

import types
import urllib2
import psycopg2.extras
import psycopg2 as pg
from bs4 import BeautifulSoup
from config import *
from siemtools import utils

LOGGER = utils.initLogger(LOG_ROUTE)


def value_data_msg(url_list, batch_id):
    """
    楼盘测评信息获取
    :param url_list:
    :return:
    """
    value_dict_list = []
    try:
        for i in range(len(url_list)):
            data_url = []
            value_title = []
            value_note = []
            html = urllib2.urlopen(url_list[i]).read()
            soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            build_name = soup.find("h1").text
            for i in soup.find_all(class_="main-mod"):
                for d in i.find_all("a", class_="fl"):
                    if d.get("href") not in data_url:
                        data_url.append(d.get("href"))
                for d in i.find_all("h3"):
                    value_title.append(d.text)
                for d in i.find_all(class_="info-desc"):
                    value_note.append(d.text)
            for i in range(len(data_url)):
                value_dict = {}
                value_dict["build_name"] = build_name
                value_dict["batch_id"] = batch_id
                value_dict["value_url"] = data_url[i]
                value_dict["evaluate_title"] = value_title[i].replace("\n", " ")
                value_dict["evaluate_note"] = value_note[i].replace("\n", " ")
                value_dict_list.append(value_dict)
        return value_dict_list
    except Exception, ex:
        LOGGER.error("build value msg get failed,msg: "+str(ex))
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
            print data_dict[i]
            cur.execute(ajk_data_sql(table_name, data_dict[i]))
        conn.commit()
        return True
    except Exception, ex:
        LOGGER.error("ajk_data insert failed,msg{0:s}".format(str(ex)))
        # raise Exception(str(ex))

# d_d = value_data_msg(d_l)
# ajk_data_insert("g", d_d)
