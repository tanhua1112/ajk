# coding: utf-8
"""
获取安居客楼盘名称、URL信息
"""

import types
import urllib2
import psycopg2 as pg
import psycopg2.extras
from bs4 import BeautifulSoup
from siemtools import utils
from config import *
import time

batch_time = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
batch_id = "AJK_DATA_{0:s}_1".format(batch_time)
LOGGER = utils.initLogger(LOG_ROUTE)


def ajk_page_url(baseurl):
    """
    获取安居客标签页URL
    :param baseurl:安居客URL
    :return:
    """
    page_list = [baseurl]
    while 1:
        html = urllib2.urlopen(baseurl).read()
        soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
        if soup.find(class_="pagination").find("a", "next-page next-link"):
            next_page = soup.find(class_="pagination").find("a", "next-page next-link").get("href")
            page_list.append(next_page)
            baseurl = next_page
        else:
            break
    return page_list


def ajk_data_url(page_list, batch_id):
    """
    获取楼盘URL、楼盘名称
    :param page_list: 标签页URL
    :return:
    """
    ajk_data_list = []
    for i in range(len(page_list)):
        html = urllib2.urlopen(page_list[i])
        soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
        for a in soup.find(class_="key-list").find_all("a", "lp-name"):
            ajk_data_dict = {}
            ajk_data_dict["batch_id"] = batch_id
            ajk_data_dict["build_url"] = a.get("href")
            ajk_data_dict["build_name"] = a.find("h3").text
            ajk_data_list.append(ajk_data_dict)
    return ajk_data_list


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


def ajk_type_url(data_d):
    """
    获取楼盘信息类别URL
    :param data_d: ajk_url 数据
    :return:
    """
    type_list = []
    try:
        for i in range(len(data_d)):
            key_list = []
            value_list = []
            type_dict = {}
            baseurl = data_d[i].get("build_url")
            print i, baseurl
            type_dict["build_name"] = data_d[i].get("build_name")
            html = urllib2.urlopen(baseurl).read()
            soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            for i in soup.find_all(class_="lp-navtabs-warp"):
                key_list = i.text.strip().replace(" ","").split("\n")
            for a in soup.find(class_="lp-navtabs-warp").find_all("a"):
                value_list.append(a.get("href"))
            for i in range(len(key_list)):
                if key_list[i] in BUILD_INFO_DICT:
                    type_dict[BUILD_INFO_DICT[key_list[i]]] = value_list[i]
            type_list.append(type_dict)
        return type_list
    except Exception, ex:
        LOGGER.error("ajk_type url get failed,msg:{0:s}".format(str(ex)))
        # raise Exception(str(ex))
