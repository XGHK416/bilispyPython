# -*- coding: UTF-8 -*-
# 初始化爬取

# import txt_io
import logging

import sys
import time

from Flask.spider import api_url as api
from Flask.spider import package
from Flask.util import prase_content
import random
from Flask.sql import table_sql, data_rank_sql
from Flask.sql.do_sql import Db
from Flask.item import global_val as gl
import traceback

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
        db.insert_or_update(i.get('mid'), table_sql.insert_user_detect())
        START_NUM = START_NUM + 1

        gl.set_value('current_user', START_NUM)

    # 随机抽取一个人并开始下一个迭代
    user_list = user_following + user_follower
    random_user = user_list[random.randint(0, len(user_list) - 1)]
    # 判断爬取人数是否够
    if START_NUM < MAX_USER_NUM:
        return init_parse_user(random_user['mid'])
    else:
        return


# 更新用户
def update_parse_user():
    global db
    db.start_sql_engine()
    user_list = db.select(table_sql.query_detect_list(0))
    # print(list(user_list))
    gl.set_value('total_user', len(user_list))
    for index, mid in enumerate(list(user_list)):
        try:
            parse_user_info(mid[0])
            gl.set_value('current_user', index + 1)
        except Exception as e:
            print(traceback.format_exc())
            continue
    db.close_db()


# 将用户基本信息插入数据库并返回用户对象，被调用
def parse_user_info(mid):
    # print(mid)
    gl.set_value("current_id", "mid" + str(mid))
    global MAX_USER_NUM, START_NUM, db
    # print(mid)
    # 用户基本信息解析
    # print(1)
    user_info_json = prase_content.return_json(api.return_user_info(mid), None, return_header())
    time.sleep(random.uniform(0.2, 0.4))
    # print(2)
    user_info_ff_json = prase_content.return_json(api.return_user_follower_following(mid), None, return_header())
    time.sleep(random.uniform(0.2, 0.4))
    # print(3)
    user_video_count_json = prase_content.return_json(api.return_user_video_count(mid, None), None, return_header())
    # print(4)
    if user_info_json is None or user_info_ff_json is None or user_video_count_json is None:
        raise Exception(str(mid) + "遭遇反扒")
    # 用户不存在，或无意义账号
    # print(user_info_json)
    if user_info_json.get('code') != 0:
        db.insert_or_update(item=None, sql=table_sql.delete_detect_user(mid))
        return

    user_video_count = user_video_count_json.get('data').get('count')

    # print("user_video_count: " + str(user_video_count_json))
    user_info = package.package_user_info(user_info_json, user_info_ff_json, user_video_count)
    user_official = package.package_user_official(user_info_json)

    db.insert_or_update(item=user_info.return_tup(), sql=table_sql.insert_user_info())
    db.insert_or_update(item=user_official.return_tup(), sql=table_sql.replace_user_official())

    # 用户视频主要分布统计
    user_video_category = user_video_count_json.get('data').get('tlist')
    if len(user_video_category) == 0:
        return
    elif isinstance(user_video_category, dict):
        for i in user_video_category:
            uv_info = package.package_video_count(user_video_category[i], user_info_json.get('data').get('mid'))
            db.insert_or_update(item=uv_info.return_tup(), sql=table_sql.replace_uv_count())
    elif isinstance(user_video_category, list):
        for index, i in enumerate(user_video_category):
            uv_info = package.package_video_count(user_video_category[index], user_info_json.get('data').get('mid'))
            db.insert_or_update(item=uv_info.return_tup(), sql=table_sql.replace_uv_count())


#              用户 上 |视频 下


# 更新视频 由添加新视频检测和更新视频检测组成
def update_video():
    global db
    db.start_sql_engine()

    # 对数据库里需要更新的数据进行爬取
    need_update_id_list = db.select(table_sql.query_update_video_list())
    if len(need_update_id_list) != 0:
        gl.set_value('total_video', len(need_update_id_list))
        for update_aid in need_update_id_list:
            try:
                gl.set_value('current_video', gl.get_value('current_video') + 1)
                update_old_video(update_aid[0])
            except Exception as e:
                logging.error(update_aid[0], e)
                continue
    time.sleep(120)
    # 检查所有爬取用户有没有更新视频
    user_list = db.select(table_sql.query_detect_list(0))
    for mid in user_list:
        try:
            insert_new_video(mid[0])
        except Exception as e:
            logging.error(str(mid[0]), e)
            continue

    db.close_db()


# 添加用户新视频检测
def insert_new_video(mid):
    # print('mid:'+str(mid))
    gl.set_value("current_id", "mid" + str(mid))
    global db
    yesterday_video_count = db.select(table_sql.query_yesterday_user_video_count(mid))
    # print("len:"+str(yesterday_video_count))
    if len(yesterday_video_count) == 0:
        # 该天的数据缺失
        return
    yesterday_video_count = yesterday_video_count[0][0]
    ##################
    current_video_count_json = prase_content.return_json(api.return_user_video_count(mid, None), None, return_header())
    # if not current_video_count_json.get('status'):
    #     # 请求失败者再次请求
    #     time.sleep(20)
    #     current_video_count_json = prase_content.return_json(api.return_user_video_count(mid, None), None,
    #                                                          return_header())
    ##################
    time.sleep(0.2)
    current_video_count = current_video_count_json.get('data').get('count')
    if yesterday_video_count < current_video_count:
        pagesize = (current_video_count - yesterday_video_count) if (
                (current_video_count - yesterday_video_count) < 100) else 100
        #############
        current_video_list_json = prase_content.return_json(
            api.return_user_video_count(mid, pagesize), None, return_header())
        # if not current_video_list_json.get('status'):
        #     time.sleep(20)
        #     current_video_list_json = prase_content.return_json(
        #         api.return_user_video_count(mid, pagesize), None, return_header())
        #############
        video_list = current_video_list_json.get('data').get('vlist')
        for more_video in range(pagesize):
            try:
                aid = video_list[more_video].get('aid')
                # print('aid'+str(aid))
                gl.set_value('current_video', gl.get_value('current_video') + 1)
                gl.set_value('total_video', gl.get_value('current_video'))
                # 添加视频监控
                new_video_detect(aid)
            except IndexError as exc:
                logging.error(str(mid), exc)
                continue


# 更新视频检测，被调用
def update_old_video(aid):
    gl.set_value("current_id", "aid" + str(aid))
    global db
    video_json = prase_content.return_json(api.return_video_info(aid), None, return_header())
    # 视频不存在，或以删除，则让视频侦测完毕
    if video_json.get('code') != 0:
        db.insert_or_update(item=None, sql=table_sql.update_complete_video_detect(aid))
        return
    video_info = package.package_video_info(video_json)
    db.insert_or_update(item=video_info.return_tup(), sql=table_sql.insert_video_info())
    db.insert_or_update(item=None, sql=table_sql.update_video_detect_time(aid))


# 添加新视频检测
def new_video_detect(aid):
    global db
    if db.insert_or_update(item=aid, sql=table_sql.insert_detect_video()):
        # 插入视频数据
        ############
        video_json = prase_content.return_json(api.return_video_info(aid), None, return_header())
        # print('video_json', video_json)
        # if video_json.get('code') != 0:
        #     time.sleep(20)
        #     video_json = prase_content.return_json(api.return_video_info(aid), None, return_header())
        # if video_json.get('code') != 0:
        #     return
        ############
        video_info = package.package_video_info(video_json)
        video_bvid = package.package_video_bvid(video_json)
        db.insert_or_update(item=video_info.return_tup(), sql=table_sql.insert_video_info())
        db.insert_or_update(item=video_bvid.return_tup(),sql=table_sql.insert_video_bvid())


# rank
def video_rank_update():
    global db
    result = db.select(data_rank_sql.query_video())
    for item in result:
        try:
            view = item[7]
            favorite = item[8]
            coins = item[9]
            like = item[11]

            video_id = item[1]
            uploader_id = item[17]
            section = item[3]
            score = format(view * 0.8 + (coins * 0.3 + like * 0.3 + favorite * 0.3) * 100 * 0.2, '.2f')
            db.insert_or_update((video_id, score, section, uploader_id), data_rank_sql.insert_video_rank())
        except Exception:
            continue


def uploader_rank_update():
    global db
    result = db.select(data_rank_sql.query_uploader())
    for item in result:
        try:
            uploader_id = item[1]
            section_tuple = db.select(data_rank_sql.query_uploader_video_section(uploader_id))
            if len(section_tuple) != 0:
                section = section_tuple[0][0]
                if section is None:
                    section = '未分区'
            else:
                section = '未分区'
            # print(section)

            video_score_tuple = db.select(data_rank_sql.query_uploader_video_score(uploader_id))
            if len(video_score_tuple) != 0:
                video_score = video_score_tuple[0][0]
                if video_score is None:
                    video_score = 0
            else:
                video_score = 0
            uploader_score = item[11] * 0.5
            score = int(int(video_score) * 10000 * 0.5 + int(uploader_score) * 1000)
            db.insert_or_update((uploader_id, score, section), data_rank_sql.insert_uploader_rank())
        except Exception:
            continue

def rank_update():
    global db
    db.start_sql_engine()
    video_rank_update()
    uploader_rank_update()
    db.close_db()


if __name__ == '__main__':
    gl._init()
    db.start_sql_engine()
    update_video()
    db.close_db()
    # db.close_db()
