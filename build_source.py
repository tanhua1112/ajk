# coding: utf-8
"""
安居客楼盘房源
"""

import types
import urllib2
import psycopg2.extras
import psycopg2 as pg
from bs4 import BeautifulSoup
from config import *
from siemtools import utils

LOGGER = utils.initLogger(LOG_ROUTE)


def build_source_page(baseurl):
    """
    楼盘房源数据标签页获取
    :param baseurl:安居客URL
    :return:
    """
    user_agent = '"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"'
    headers = {'User-Agent': user_agent}
    page_list = []
    first_page = baseurl
    while 1:
        req = urllib2.Request(baseurl, headers=headers)
        html = urllib2.urlopen(req).read()
        soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
        if soup.find(class_="pagination"):
            if soup.find(class_="pagination").find("a", "next-page next-link"):
                next_page = soup.find(class_="pagination").find("a", "next-page next-link").get("href")
                page_list.append(next_page)
                baseurl = next_page
            else:
                page_list.append(first_page)
                break
        elif soup.find(class_="no_result-info"):
            LOGGER.error("{0:s} build source no-exist".format(baseurl))
            print "no-exist"
            break
        else:
            break
    return page_list


def build_source_data(page_list):
    """
    楼盘房源数据获取
    :param page_list:
    :return:
    """
    user_agent = '"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"'
    headers = {'User-Agent': user_agent}
    source_data_url = []
    try:
        for i in range(len(page_list)):
            req = urllib2.Request(page_list[i], headers=headers)
            html = urllib2.urlopen(req).read()
            soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            for i in soup.find_all("div", class_="p2"):
                for d in i.find_all("a",class_="items_l"):
                    source_data_url.append(d.get("href"))
        return source_data_url
    except Exception, ex:
        LOGGER.error("build source data get failed,msg:{0:s}".format(str(ex)))
        # raise Exception(str(ex))


def build_source_msg(url_list, batch_id):
    """
    获取楼盘房源数据信息
    :param data_list:
    :return:
    """
    user_agent = '"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"'
    headers = {'User-Agent': user_agent}
    source_data_list = []
    try:
        for i in range(len(url_list)):
            source_data = {}
            type_list = []
            data_list = []
            req = urllib2.Request(url_list[i], headers=headers)
            html = urllib2.urlopen(req).read()
            soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            for d in soup.find_all(class_="attr"):
                type_list.append(d.text)
                print d.text
            for d in soup.find_all(class_="value"):
                data_list.append(d.text.strip())
            for i in range(len(type_list)):
                if type_list[i] in BUILD_INFO_DICT:
                    source_data[BUILD_INFO_DICT[type_list[i]]] = data_list[i].replace("\n", " ")
                source_data["batch_id"] = batch_id
            source_data_list.append(source_data)
        return source_data_list
    except Exception, ex:
        LOGGER.error("build source data get failed,msg:{0:s}".format(str(ex)))
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


# d_l = [u'https://heb.fang.anjuke.com/loupan/fangyuan-411852.html', u'https://heb.fang.anjuke.com/loupan/fangyuan-253948.html', u'https://heb.fang.anjuke.com/loupan/fangyuan-417997.html', u'https://heb.fang.anjuke.com/loupan/fangyuan-430815.html', u'https://heb.fang.anjuke.com/loupan/fangyuan-412237.html', u'https://heb.fang.anjuke.com/loupan/fangyuan-253883.html', u'https://heb.fang.anjuke.com/loupan/fangyuan-418732.html', u'https://heb.fang.anjuke.com/loupan/fangyuan-253847.html', u'https://heb.fang.anjuke.com/loupan/fangyuan-417422.html', u'https://heb.fang.anjuke.com/loupan/fangyuan-253924.html']
# for i in range(len(d_l)):
#     print i
#     page_list = build_source_page(d_l[i])
#     print page_list
#     data_url = build_source_data(page_list)
#     print data_url
#     d_l = build_source_msg(data_url, "batch_id")
#     print d_l
