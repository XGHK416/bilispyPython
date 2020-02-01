# -*- coding: UTF-8 -*-
# 初始化爬取

# import txt_io
import logging

import sys
from Flask.spider import api_url as api
from Flask.spider import package
from Flask.util import prase_content
import random
from Flask.sql import table_sql
from Flask.sql.do_sql import Db
from Flask.item import global_val as gl

INIT_USER = 3043120
MAX_USER_NUM = 100000
START_NUM = 0

db = Db()

sys.setrecursionlimit(9000000)


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
    user_following = []
    user_follower = []
    db.insert_or_update(mid, table_sql.insert_user_detect())
    # 准备下一个迭代
    # 用户关注与被关注列表
    user_following_json = prase_content.return_json(api.return_user_follow(1, 10, mid), None,
                                                    return_header())
    user_follower_json = prase_content.return_json(api.return_user_fans(1, 10, mid), None,
                                                   return_header())
    try:
        user_following = user_following_json.get('data').get('list')
        user_follower = user_follower_json.get('data').get('list')

    except AttributeError as aerr:
        logging.exception(aerr)
    # 将关注的人放入数据库，即这些人为爬取对象
    for i in user_following:
        # print(i.get('mid'))
        # parse_user_info(i.get('mid'))
        db.insert_or_update(i.get('mid'), table_sql.insert_user_detect())
        START_NUM = START_NUM + 1
        gl.set_value('CURRENT_USER_NUM', START_NUM)

    # 随机抽取一个人并开始下一个迭代
    user_list = user_following + user_follower
    random_user = user_list[random.randint(0, len(user_list) - 1)]
    # 判断爬取人数是否够
    if START_NUM < MAX_USER_NUM:
        return init_parse_user(random_user['mid'])
    else:
        return


# 之后更新用户
def update_parse_user():
    global db
    db.start_sql_engine()
    user_list = db.select(table_sql.query_detect_list(0))
    # print(list(user_list))
    for index, mid in enumerate(list(user_list)):
        parse_user_info(mid[0])
        gl.set_value('CURRENT_USER_NUM', index + 1)
    db.close_db()


# 将用户基本信息插入数据库并返回用户对象，被调用
def parse_user_info(mid):
    global MAX_USER_NUM, START_NUM, db

    # 用户基本信息解析
    user_info_json = prase_content.return_json(api.return_user_info(mid), None, return_header())
    user_info_ff_json = prase_content.return_json(api.return_user_follower_following(mid), None, return_header())
    # 用户不存在，或无意义账号
    if user_info_json.get('code') != 0:
        db.insert_or_update(item=None, sql=table_sql.delete_detect_user(mid))
        return
    user_video_count_json = prase_content.return_json(api.return_user_video_count(mid, None), None, return_header())
    user_video_count = user_video_count_json.get('data').get('count')
    user_object = package.package_user_info(user_info_json, user_info_ff_json, user_video_count)
    user_official = package.package_user_official(user_info_json)

    db.insert_or_update(item=user_object.return_tup(), sql=table_sql.insert_user_info())
    db.insert_or_update(item=user_official.return_tup(), sql=table_sql.replace_user_official())

    # 用户视频主要分布统计
    user_video_category = user_video_count_json.get('data').get('tlist')
    for i in user_video_category:
        uv_info = package.package_video_count(user_video_category[i], user_info_json.get('data').get('mid'))
        db.insert_or_update(item=uv_info.return_tup(), sql=table_sql.replace_uv_count())
    return user_object


#              用户 上 |视频 下


# 更新视频 由添加新视频检测和更新视频检测组成
def update_video():
    global db
    db.start_sql_engine()

    # 对数据库里需要更新的数据进行爬取
    need_update_id_list = db.select(table_sql.query_update_video_list())
    if len(need_update_id_list) != 0:
        # print('更新人数为：'+str(len(need_update_id_list)))
        gl.set_value('CURRENT_VIDEO_NUM', gl.get_value('CURRENT_VIDEO_NUM') + len(need_update_id_list))
        for update_aid in need_update_id_list:
            update_old_video(update_aid[0])

    # 检查所有爬取用户有没有更新视频
    user_list = db.select(table_sql.query_detect_list(0))
    # print(user_list)
    for mid in user_list:
        insert_new_video(mid[0])

    db.close_db()


# 添加用户新视频检测
def insert_new_video(mid):
    global db
    yesterday_video_count = db.select(table_sql.query_yesterday_user_video_count(mid))
    if len(yesterday_video_count) == 0:
        # 该天的数据缺失
        return
    # print(yesterday_video_count)
    yesterday_video_count = yesterday_video_count[0][0]
    # print(yesterday_video_count)
    # print('mid: '+str(mid)+'; 昨日视频数:'+str(yesterday_video_count))
    # print(yesterday_video_count)
    current_video_count_json = prase_content.return_json(api.return_user_video_count(mid, None), None, return_header())
    current_video_count = current_video_count_json.get('data').get('count')
    current_video_list_json = prase_content.return_json(
        api.return_user_video_count(mid, current_video_count - yesterday_video_count), None, return_header())
    # print('更新数: '+str(current_video_count - yesterday_video_count))
    if yesterday_video_count < current_video_count:
        # print()
        video_list = current_video_list_json.get('data').get('vlist')
        for more_video in range(current_video_count - yesterday_video_count):
            aid = video_list[more_video].get('aid')
            # 添加视频监控
            new_video_detect(aid)
            # gl.set_value('NEW_ADD_VIDEO_NUM', gl.get_value('NEW_ADD_VIDEO_NUM') + 1)


# 更新视频检测，被调用
def update_old_video(aid):
    # print('更新已有视频：'+str(aid))
    video_json = prase_content.return_json(api.return_video_info(aid), None, return_header())
    # 视频不存在，或以删除，则让视频侦测完毕
    if video_json.get('code') != 0:
        db.insert_or_update(item=None, sql=table_sql.update_complete_video_detect(aid))
        return
    video_info = package.package_video_info(video_json)
    db.insert_or_update(item=video_info.return_tup(), sql=table_sql.insert_video_info())
    db.insert_or_update(item=None, sql=table_sql.update_video_detect_time(aid))
    # print('更新结束')


# 添加新视频检测，被调用
def new_video_detect(aid):
    gl.set_value('CURRENT_VIDEO_NUM', gl.get_value('CURRENT_VIDEO_NUM') + 1)
    db.insert_or_update(item=aid, sql=table_sql.insert_detect_video())
    # 插入视频数据
    video_json = prase_content.return_json(api.return_video_info(aid), None, return_header())
    video_info = package.package_video_info(video_json)
    db.insert_or_update(item=video_info.return_tup(), sql=table_sql.insert_video_info())


if __name__ == '__main__':
    init_parse_data()
