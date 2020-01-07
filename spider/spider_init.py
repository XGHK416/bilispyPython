# -*- coding: UTF-8 -*-
# 初始化爬取


from spider import api_url as api
from spider import package
from util import prase_content
from sql import table_sql
from sql.do_sql import Db

INIT_USER = 3043120


def return_header():
    header = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        "Cookie": "UM_distinctid=167efec6114127-0b5ca80fa5777e-b781636-1fa400-167efec611586f;__guid=74616212.3534962106793367000.1553586436247.447;joymeid=5b562df428c0d3c616f9125854603cc8;test_cookie_enable=null;CNZZDATA1274517832=1248405128-1553585977-https%253A%252F%252Fwww.baidu.com%252F%7C1553672138"
    }
    return header


# 解析数据
def parse_data():
    db = Db()
    db.start_sql_engine()
    # 业务逻辑开始
    text = prase_content.return_html(api.return_user_info(INIT_USER), None, return_header())
    json_data = prase_content.html_to_json(text)
    user_object = package.package_user_info(json_data)
    db.insert(item=user_object, sql=table_sql.user_info())
    # 业务逻辑结束
    db.close_db()

# todo 文件读入


if __name__ == '__main__':
    parse_data()
