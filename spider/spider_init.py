# -*- coding: UTF-8 -*-
# 初始化爬取
import time

import txt_io
from spider import api_url as api
from spider import package
from util import prase_content
import random
from sql import table_sql
from sql.do_sql import Db

INIT_USER = 3043120
MAX_USER_NUM = 10
START_NUM = 0

db = Db()


def return_header():
    header = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        "Cookie": "UM_distinctid=167efec6114127-0b5ca80fa5777e-b781636-1fa400-167efec611586f;__guid=74616212.3534962106793367000.1553586436247.447;joymeid=5b562df428c0d3c616f9125854603cc8;test_cookie_enable=null;CNZZDATA1274517832=1248405128-1553585977-https%253A%252F%252Fwww.baidu.com%252F%7C1553672138"
    }
    return header


# 第一次爬取入口
def init_parse_data():
    global db
    db.start_sql_engine()
    init_parse_user(INIT_USER)
    db.close_db()


# 第一次爬取用户
def init_parse_user(mid):
    global MAX_USER_NUM, START_NUM, db
    parse_user_info(mid)

    # 准备下一个迭代
    # 用户关注与被关注列表
    user_following = prase_content.return_json(api.return_user_follow(1, 10, mid), None,
                                               return_header()).get('data').get('list')
    user_follower = prase_content.return_json(api.return_user_fans(1, 10, mid), None,
                                              return_header()).get('data').get('list')
    # 将关注的人放入数据库，即这些人为爬取对象
    for i in user_following:
        parse_user_info(i.get('mid'))
        START_NUM = START_NUM + 1
    # 随机抽取一个人并开始下一个迭代
    user_list = user_following + user_follower
    random_user = user_list[random.randint(0, len(user_list) - 1)]
    # 判断爬取人数是否够
    if START_NUM < MAX_USER_NUM:
        init_parse_user(random_user['mid'])
    else:
        return


# 之后更新用户
def update_parse_user():
    global db
    db.start_sql_engine()
    user_list = txt_io.read_from_txt()
    for mid in user_list:
        parse_user_info(mid)
    db.close_db()


# 将用户基本信息插入数据库并返回用户对象
def parse_user_info(mid):
    global MAX_USER_NUM, START_NUM, db

    # 用户基本信息解析
    print(mid)
    user_info_json = prase_content.return_json(api.return_user_info(mid), None, return_header())
    user_info_ff_json = prase_content.return_json(api.return_user_follower_following(mid), None, return_header())
    user_video_count_json = prase_content.return_json(api.return_user_video_count(mid), None, return_header())
    user_video_count = user_video_count_json.get('data').get('count')
    user_object = package.package_user_info(user_info_json, user_info_ff_json, user_video_count)
    user_official = package.package_user_official(user_info_json)

    db.insert(item=user_object.return_tup(), sql=table_sql.user_info(user_object.user_id))
    db.insert(item=user_official.return_tup(), sql=table_sql.user_official())

    txt_io.write_in_txt(user_object.user_id)

    # 用户视频主要分布统计
    user_video_category = user_video_count_json.get('data').get('tlist')
    for i in user_video_category:
        uv_info = package.package_video_count(user_video_category[i], user_info_json.get('data').get('mid'))
        db.insert(item=uv_info.return_tup(), sql=table_sql.uv_count())

    return user_object


#              用户 上 |视频 下


# 更新视频 由添加新视频检测和更新视频检测组成
def update_video():
    global db
    db.start_sql_engine()

    # 对数据库里需要更新的数据进行爬取
    need_update_id_list = db.select(table_sql.query_update_video_list())
    for update_aid in need_update_id_list:
        update_old_video(update_aid)

    # 检查所有爬取用户有没有更新视频
    user_list = txt_io.read_from_txt()
    for mid in user_list:
        insert_new_video(mid)

    db.close_db()


# 添加用户新视频检测
def insert_new_video(mid):
    global db
    video_num = db.select(table_sql.check_update_video(mid))
    print(video_num)

    current_video_count_json = prase_content.return_json(api.return_user_video_count(mid), None, return_header())
    current_video_count = current_video_count_json.get('data').get('count')
    if video_num < current_video_count:
        video_list = current_video_count_json.get('data').get('vlist')
        for more_video in range(current_video_count - video_num):
            aid = video_list[more_video].get('aid')
            # 添加视频监控
            new_video_detect(aid)


# 更新视频检测
def update_old_video(aid):
    video_json = prase_content.return_json(api.return_video_info(aid), None, return_header())
    video_info = package.package_video_info(video_json)
    db.insert(item=video_info.return_tup(), sql=table_sql.video_info())
    db.insert(item=None, sql=table_sql.complete_detect(aid))


# 添加新视频检测
def new_video_detect(aid):
    db.insert(item=aid, sql=table_sql.add_update_video())
    # 插入视频数据
    video_json = prase_content.return_json(api.return_video_info(aid), None, return_header())
    video_info = package.package_video_info(video_json)
    db.insert(item=video_info.return_tup(), sql=table_sql.video_info())


if __name__ == '__main__':
    init_parse_data()
