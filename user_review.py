# coding: utf-8
"""
用户评论
"""
import urllib2
import types
import psycopg2.extras
import psycopg2 as pg
from bs4 import BeautifulSoup
from config import *
from siemtools import utils

LOGGER = utils.initLogger(LOG_ROUTE)


def user_words_page(baseurl):
    """
    用户评论签页URL
    :param baseurl:安居客URL
    :return:
    """
    page_list = []
    first_page = baseurl
    while 1:
        html = urllib2.urlopen(baseurl).read()
        soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
        if soup.find(class_="pagination"):
            if soup.find(class_="pagination").find("a", "next-page next-link"):
                next_page = soup.find(class_="pagination").find("a", "next-page next-link").get("href")
                page_list.append(next_page)
                baseurl = next_page
            else:
                page_list.append(first_page)
                break
        else:
            break
    return page_list


def user_words_msg(page_list, batch_id):
    """
    获取用户评论信息
    :param page_list:
    :return:
    """
    user_words_list = []
    try:
        for i in range(len(page_list)):
            html = urllib2.urlopen(page_list[i]).read()
            soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
            build_name = soup.find("h1").text
            for review_h in soup.find_all(class_="total-revlist"):
                for i in review_h.find_all(class_="info-mod"):
                    user_words_dict = {}
                    user_words_dict["batch_id"] = batch_id
                    user_words_dict["build_name"] = build_name
                    user_words_dict["user_name"] = i.find("span", class_="author").text.replace("'", " ")
                    user_words_dict["words_note"] = i.find("h4", class_="rev-subtit part-text").text.strip()
                    user_words_dict["words_time"] = i.find("span", class_="date").text
                    user_words_list.append(user_words_dict)
        return user_words_list
    except Exception, ex:
        LOGGER.error("user review get failed,msg{0:s}"+str(ex))
        # pass
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


# d_l = [u'https://heb.fang.anjuke.com/loupan/dianping-411852.html', u'https://heb.fang.anjuke.com/loupan/dianping-412237.html']
# for i in range(len(d_l)):
#     page_list = user_words_page(d_l[i])
#     data_list = user_words_msg(page_list)
#     ajk_data_insert("d", data_list)

