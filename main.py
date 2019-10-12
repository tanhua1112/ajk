# coding: utf-8

import time
from database import *
from ajk_url import *
from build_info import *
from build_type import *
from user_review import *
from build_source import *
from dynamic_info import *
from build_value import *


batch_time = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
batch_id = "AJK_DATA_{0:s}_1".format(batch_time)

print db_table_drop(DB.host, DB.port, DB.user, DB.password, DB.dbname)     # 清除数据库中的数据表
print db_table_create(DB.host, DB.port, DB.user, DB.password, DB.dbname)   # 创建数据表

page_list = ajk_page_url(AJK_BASE_URL)      # 获取安居客标签页URL
data_list = ajk_data_url(page_list, batch_id) # 获取安居客楼盘信息数据
ajk_data_insert("ajk_build", data_list)     # 插入楼盘数据信息
build_info_list = []
house_type_list = []
user_review_list = []
build_source_list = []
dynamic_info_list = []
build_value_list = []
d_l = ajk_type_url(data_list)
for i in range(len(d_l)):
    build_info_list.append(d_l[i]["build_info"])
    house_type_list.append(d_l[i]["house_type"])
    user_review_list.append(d_l[i]["user_review"])
    build_source_list.append(d_l[i]["build_source"])
    dynamic_info_list.append(d_l[i]["dynamic_info"])
    build_value_list.append(d_l[i]["build_value"])

info_data = build_info(build_info_list, batch_id)
ajk_data_insert("ajk_base_info", info_data, DB.host, DB.port, DB.user, DB.password, DB.dbname)

for i in range(len(user_review_list)):
    page_list = user_words_page(user_review_list[i])     # 获取用户点评标签页
    data_list = user_words_msg(page_list, batch_id)   # 获取用户点评数据信息
    # 插入用户点评数据
    ajk_data_insert("ajk_user_words", data_list, DB.host, DB.port, DB.user, DB.password, DB.dbname)

for i in range(len(build_source_list)):
    page_list = build_source_page(build_source_list[i])  # 获取楼盘房源标签页信息
    data_url = build_source_data(page_list)     # 获取楼盘房源URL
    source_list = build_source_msg(data_url, batch_id)    # 获取楼盘房源信息
    # 插入楼盘房源信息数据
    ajk_data_insert("ajk_build_resource", source_list, DB.host, DB.port, DB.user, DB.password, DB.dbname)

for i in range(len(dynamic_info_list)):
    url_list = dynamic_data_url(dynamic_info_list[i])    # 获取楼盘动态资讯URL
    data_list = dynamic_data_msg(url_list, batch_id)  # 获取楼盘动态资讯数据
    # 插入楼盘动态资讯数据
    ajk_data_insert("ajk_dynamic_info", data_list, DB.host, DB.port, DB.user, DB.password, DB.dbname)

value_data = value_data_msg(build_value_list, batch_id)    # 获取楼盘评测数据信息
# 插入楼盘评测数据
ajk_data_insert("ajk_build_evaluate", value_data, DB.host, DB.port, DB.user, DB.password, DB.dbname)

for i in range(len(house_type_list)):
    time.sleep(1)
    page_list = build_type_page(house_type_list[i])     # 获取楼盘户型标签页
    data_list = build_type_url(page_list)   # 获取户型URL
    dict_list = type_data_msg(data_list, batch_id)    # 获取户型信息
    # 向数据库中插入户型信息
    ajk_data_insert("ajk_house_type", dict_list, DB.host, DB.port, DB.user, DB.password, DB.dbname)
