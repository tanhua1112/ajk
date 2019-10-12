# coding: utf-8
'''
获取安居客动态资讯
'''

import types
import urllib2
import psycopg2.extras
import psycopg2 as pg
from bs4 import BeautifulSoup
from config import *
from siemtools import utils

LOGGER = utils.initLogger(LOG_ROUTE)
BUILD_NAME = ""


def dynamic_data_url(baseurl):
    '''
    获取动态资讯url
    :param baseurl:
    :return:
    '''
    global BUILD_NAME
    data_url = []
    try:
        html = urllib2.urlopen(baseurl).read()
        soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
        BUILD_NAME = soup.find("h1").text
        for d in soup.find_all("div", class_="clickable sale"):
            data_url.append(d.get("link"))
        return data_url
    except Exception, ex:
        LOGGER.error("dynamic info url get failed,msg :"+str(ex))
        # raise Exception(str(ex))
        # pass


def dynamic_data_msg(url_list, batch_id):
    '''
    获取动态资讯消息内容
    :param baseurl:
    :return:
    '''
    global BUILD_NAME
    dynamic_data_list = []
    try:
        for i in range(len(url_list)):
            dynamic_data = {}
            dynamic_data["batch_id"] = batch_id
            dynamic_data["dynamic_url"] = url_list[i]
            html = urllib2.urlopen(url_list[i]).read()
            soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            dynamic_data["build_name"] = BUILD_NAME
            for d in soup.find_all("div", class_="news-detail"):
                dynamic_data["dynamic_info_title"] = d.find("h1").text.replace("\n", " ")
            for d in soup.find_all("div", class_="infos"):
                dynamic_data["dynamic_info_note"] = d.text.strip().replace("\n", " ")
            dynamic_data_list.append(dynamic_data)
        BUILD_NAME = ""
        return dynamic_data_list
    except Exception, ex:
        LOGGER.error("dynamic info url get failed,msg :"+str(ex))
        return False


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
        pass
        # raise Exception(str(ex))


# url_list = dynamic_data_url("https://heb.fang.anjuke.com/loupan/officialnews-253847.html?from=loupan_tab")
# data_list = dynamic_data_msg(url_list)
# ajk_data_insert("f", data_list)
