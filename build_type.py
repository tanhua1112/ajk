# coding: utf-8
"""
楼盘户型信息表格
"""

import types
import urllib2
import psycopg2.extras
import psycopg2 as pg
from bs4 import BeautifulSoup
from siemtools import utils
from config import *

LOGGER = utils.initLogger(LOG_ROUTE)


def build_type_page(baseurl):
    """
    获取楼盘户型标签页
    :param baseurl: 安居客户型URL
    :return:
    """
    user_agent = '"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"'
    headers = {'User-Agent': user_agent}
    page_list = [baseurl]
    while 1:
        req = urllib2.Request(baseurl, headers=headers)
        html = urllib2.urlopen(req).read()
        soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
        if soup.find(class_="pagination"):
            if soup.find(class_="pagination").find("a", class_="next-page next-link"):
                next_page = soup.find(class_="pagination").find("a", "next-page next-link").get("href")
                page_list.append(next_page)
                baseurl = next_page
            else:
                break
        else:
            break
    return page_list


def build_type_url(page_list):
    """
    获取户型URL
    :param page_list: 户型标签页URL
    :return:
    """
    user_agent = '"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"'
    headers = {'User-Agent': user_agent}
    data_url_list = []
    try:
        for i in range(len(page_list)):
            req = urllib2.Request(page_list[i], headers=headers)
            html = urllib2.urlopen(req).read()
            soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            for msg_d in soup.find_all(class_="hx-list-mod"):
                if msg_d.find('a'):
                    for i in msg_d.find_all('a'):
                        data_url_list.append(i.get("href"))
                else:
                    LOGGER.info("build type is none")
        return data_url_list
    except Exception, ex:
        LOGGER.error("build_type data url get failed,msg{0:s}:".format(str(ex)))
        # raise Exception(str(ex))


def type_data_msg(data_url_list, batch_id):
    """
    户型信息获取
    :param data_url_list:
    :return:
    """
    user_agent = '"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"'
    headers = {'User-Agent': user_agent}
    type_data_list = []
    try:
        for i in range(len(data_url_list)):
            type_dict = {}
            req = urllib2.Request(data_url_list[i], headers=headers)
            html = urllib2.urlopen(req).read()
            soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            type_dict["batch_id"] = batch_id
            type_dict["build_name"] = \
                soup.find("h1").text if soup.find("h1") else u""
            type_dict["photo_title"] = \
                soup.find(class_="hx-de-right").find("span").text.strip().replace(" ", "").replace("\n", " ")\
                    if soup.find(class_="hx-de-right") else u""
            type_dict["build_msg"] = \
                soup.find(class_="hx-detail-wrap").text.strip().replace(" ", "").replace("\n", " ")\
                    if soup.find(class_="hx-detail-wrap") else u""
            type_dict["build_info"] = soup.find(class_="hx-des-wrap").text.strip().replace(" ", "").replace("\n", " ")\
                if soup.find(class_="hx-des-wrap") else u""
            type_data_list.append(type_dict)
        return type_data_list
    except Exception, ex:
        LOGGER.error("build type info get failed,msg:{0:s}".format(str(ex)))
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


# d_l = ["https://heb.fang.anjuke.com/loupan/huxing-417422.html"]
# for i in range(len(d_l)):
#     page_list = build_type_page(d_l[i])
#     print page_list
#     data_list = build_type_url(page_list)
#     print data_list
#     dict_list = type_data_msg(data_list)
#     print dict_list
#     ajk_data_insert("a", dict_list)
