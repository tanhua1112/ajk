# coding: utf-8

LOG_ROUTE = "ajk_data.log"

# 创建数据表
CREATE_AJK_TABLE = """--
       --楼盘名称URL表格
       --
       CREATE TABLE ajk_build(
       id serial NOT NULL,  --序列号
       batch_id character varying(40) NOT NULL, --数据投放批次标号
       build_url character varying(50) NOT NULL,  --楼盘链接
       build_name character varying(50) NOT NULL, --楼盘名称
       r_time timestamp without time zone DEFAULT now(), --数据上传时间
       CONSTRAINT "AJK_11" PRIMARY KEY (batch_id, build_name)
       );"""
CREATE_BASE_MSG = """--
       --楼盘详情表格
       --
       CREATE TABLE ajk_base_info(
       id serial NOT NULL,  --序列号
       batch_id character varying(30) NOT NULL,
       build_name character varying(50) NOT NULL,
       build_point text,
       unit_price text,
       total_price text,
       prop_type text,
       develop_name text,
       local_area character varying(20),
       build_address text,
       sale_num character varying(25),
       lowest_pay text,
       mouth_pay text,
       build_preferential text,
       house_type text,
       sale_time text,
       live_time text,
       sale_address text,
       sale_license text,
       build_type text,
       use_time text,
       plot_ratio character varying(50),
       green_coverage text,
       user_num text,
       build_status text,
       job_schedule text,
       prop_cost text,
       prop_name text,
       car_num text,
       car_rate text,
       build_photo text,
       r_time timestamp without time zone DEFAULT now()
       );"""
CREATE_HOUSE_TYPE = """--
       --房屋户型列表
       --
       CREATE TABLE ajk_house_type(
       id serial NOT NULL,  --序列号
       batch_id character varying(40) NOT NULL,
       build_name text NOT NULL,
       photo_title text,
       build_msg text,
       build_info text,
       r_time timestamp without time zone DEFAULT now()
       );"""
CREATE_USER_WORDS = """--
       --用户点评
       --
       CREATE TABLE ajk_user_words(
       id serial NOT NULL,  --序列号
       batch_id character varying(40) NOT NULL,
       build_name text,
       user_name text,
       words_note text,
       words_time text,
       r_time timestamp without time zone DEFAULT now()
       );"""
CREATE_BUILD_RESOURCE = """--
       --楼盘房源信息表格
       --
       CREATE TABLE ajk_build_resource(
       id serial NOT NULL,  --序列号
       batch_id character varying(40) NOT NULL,
       build_name text NOT NULL,
       sale_price text,
       house_type text,
       build_preferential text,
       build_size text,
       lowest_pay text,
       build_dire text,
       mouth_pay text,
       build_floor text,
       prop_type text,
       build_decorate text,
       build_address text,
       live_time text,
       house_name text,
       user_num text,
       build_local text,
       build_status text,
       sale_time text,
       use_time text,
       build_type text,
       plot_ratio text,
       prop_name text,
       green_coverage text,
       property_cost text,
       car_num text,
       r_time timestamp without time zone DEFAULT now()
       );"""
CREATE_DYNAMIC_INFO = """--
       --动态资讯
       --
       CREATE TABLE ajk_dynamic_info(
       id serial NOT NULL,  --序列号
       batch_id character varying(40) NOT NULL,
       dynamic_url text,
       build_name text NOT NULL,
       dynamic_info_title text,
       dynamic_info_note text,
       r_time timestamp without time zone DEFAULT now()
       );"""
CREATE_BUILD_EVALUATE = """--
       --楼盘评测表
       --
       CREATE TABLE ajk_build_evaluate(
       id serial NOT NULL,  --序列号
       batch_id character varying(40) NOT NULL,
       build_name text NOT NULL,
       value_url text,
       evaluate_title text,
       evaluate_note text,
       r_time timestamp without time zone DEFAULT now()
       );"""

AJK_TABLE_CREATE = [CREATE_AJK_TABLE, CREATE_BASE_MSG, CREATE_HOUSE_TYPE,
                    CREATE_USER_WORDS, CREATE_BUILD_RESOURCE,
                    CREATE_DYNAMIC_INFO, CREATE_BUILD_EVALUATE]
AJK_TABLE = ["ajk_build", "ajk_base_info", "ajk_house_type", "ajk_user_words",
             "ajk_build_resource", "ajk_dynamic_info", "ajk_build_evaluate"]
AJK_BASE_URL = "https://heb.fang.anjuke.com/?from=navigation"


BUILD_INFO_DICT = {u"月供": "mouth_pay",
                   u"售价": "sale_price",
                   u"房型": "house_type",
                   u"优惠": "build_preferential",
                   u"面积": "build_size",
                   u"朝向": "build_dire",
                   u"楼层": "build_floor",
                   u"装修": "build_decorate",
                   u"地址": "build_address",
                   u"楼盘名": "build_name",
                   u"容积率": "plot_ratio",
                   u"绿化率": "green_coverage",
                   u"开发商": "develop_name",
                   u"车位数": "car_num",
                   u"车位比": "car_rate",
                   u"楼盘名称": "build_name",
                   u"楼盘特点": "build_point",
                   u"参考单价": "unit_price",
                   u"楼盘总价": "total_price",
                   u"物业类型": "prop_type",
                   u"区域位置": "local_area",
                   u"楼盘地址": "build_address",
                   u"规划户数": "user_num",
                   u"楼层状况": "build_status",
                   u"工程进度": "job_schedule",
                   u"最低首付": "lowest_pay",
                   u"楼盘优惠": "build_preferential",
                   u"楼盘户型": "house_type",
                   u"最新开盘": "sale_time",
                   u"交房时间": "live_time",
                   u"产权年限": "use_time",
                   u"物业公司": "prop_name",
                   u"楼盘图片": "build_photo",
                   u"区域板块": "build_local",
                   u"开盘时间": "sale_time",
                   u"建筑类型": "build_type",
                   u"物业费用": "property_cost",
                   u"参考首付": "lowest_pay",
                   u"参考月供": "mouth_pay",
                   u"物业管理费": "prop_cost",
                   u"售楼处电话": "sale_num",
                   u"售楼处地址": "sale_address",
                   u"预售许可证": "sale_license",
                   u"楼盘详情": "build_info",
                   u"户型": "house_type",
                   u"用户点评": "user_review",
                   u"楼盘房源": "build_source",
                   u"动态资讯": "dynamic_info",
                   u"楼盘评测": "build_value"}


class DB():
    host = "192.168.159.128"
    port = 5432
    user = "postgres"
    password = "postgres"
    dbname = "ajk_data"
