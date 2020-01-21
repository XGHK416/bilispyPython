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


# 解析函数
def parse_user(mid):
    global MAX_USER_NUM, START_NUM, db

    # 用户基本信息解析
    user_info_json = prase_content.return_json(api.return_user_info(mid), None, return_header())
    user_info_ff_json = prase_content.return_json(api.return_user_info(mid), None, return_header())
    user_video_count_json = prase_content.return_json(api.return_user_video_count(mid), None, return_header())
    user_video_count = user_video_count_json.get('data').get('count')

    user_object = package.package_user_info(user_info_json, user_info_ff_json, user_video_count)
    user_official = package.package_user_official(user_info_json)

    db.insert(item=user_object, sql=table_sql.user_info(user_object.user_id))
    db.insert(item=user_official, sql=table_sql.user_official())

    txt_io.write_in_txt(user_object.user_id)

    # 用户视频主要分布统计
    user_video_category = user_video_count_json.get('data').get('tlist')
    for i in user_video_category:
        item = package.package_video_count(user_video_category[i], user_info_json.get('data').get('mid'))
        db.insert(item=item, sql=table_sql.uv_count())

    # 准备下一个迭代
    # 用户关注与被关注列表
    user_following = prase_content.return_json(api.return_user_follow(1, 10, user_object.user_id), None,
                                               return_header()).get('data').get('list')
    user_follower = prase_content.return_json(api.return_user_fans(1, 10, user_object.user_id), None,
                                              return_header()).get('data').get('list')
    # 将关注的人放入数据库，即这些人为爬取对象
    for i in user_following:
        db.insert(item=user_object, sql=table_sql.user_info(i.get('mid')))
    # 随机抽取一个人并开始下一个迭代
    user_list = user_following + user_follower
    # print(str(len(user_following_json))+'dd'+str(len(user_follower_json))+'dd'+str(len(user_list)))
    random_user = user_list[random.randint(0, len(user_list) - 1)]
    # print(random_user['mid'])
    # 判断爬取人数是否够
    if START_NUM < MAX_USER_NUM:
        START_NUM = START_NUM + 1
        # print(START_NUM)
        parse_user(random_user['mid'])
    else:
        return


# 解析数据
def parse_data():
    global db
    db.start_sql_engine()
    parse_user(INIT_USER)
    db.close_db()


def update_video():
    global db
    db.start_sql_engine()
    # user_mid = 81777099
    # 检查所有爬取用户有没有更新视频
    user_list = txt_io.read_from_txt()
    for i in user_list:
        video_num = db.select(table_sql.check_update_video(i))
        print(video_num)

        current_video_count_json = prase_content.return_json(api.return_user_video_count(i), None, return_header())
        current_video_count = current_video_count_json.get('data').get('count')
        if video_num < current_video_count:
            video_list = current_video_count_json.get('data').get('vlist')
            for more_video in range(current_video_count - video_num):
                video_id = video_list[more_video].get('aid')
                # 添加视频监控
                db.insert(item=video_id, sql=table_sql.add_update_video())
                # 插入视频数据
                video_json = prase_content.return_json(api.return_video_info(video_id), None, return_header())
                video_info = package.package_video_info(video_json)
                db.insert(item=video_info.return_tup(), sql=table_sql.video_info())

    # 对数据库里需要更新的数据进行爬取
    need_update_id_list = db.select(table_sql.query_update_video_list())
    for update_aid in need_update_id_list:
        # 插入视频数据
        video_json = prase_content.return_json(api.return_video_info(update_aid), None, return_header())
        video_info = package.package_video_info(video_json)
        db.insert(item=video_info.return_tup(), sql=table_sql.video_info())
        db.insert(item=None, sql=table_sql.complete_detect(update_aid))

    db.close_db()


if __name__ == '__main__':
    parse_data()
    # update_video()
    # i = [1,2,3]
    # j = [2,3,56,]
    # print(len(i+j))
