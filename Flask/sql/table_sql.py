# 返回数据库语句


def insert_user_detect():
    sql = 'REPLACE INTO bili_detect(detect_id,detect_type,create_time) values (%s,0,now())'
    return sql


def query_detect_list(detect_type):
    sql = 'SELECT detect_id from bili_detect where detect_type = ' + str(detect_type) + ' ORDER BY detect_id ASC'
    return sql


#######################################
def insert_user_info():
    sql = 'INSERT INTO bili_uploader(user_id,nick_name,profile,sex,level,sign,silence,vip,birthday,video_count,follower,following,last_update) ' \
          'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now()) '
    # if user_id is not None:
    #     sql = sql + 'ON DUPLICATE KEY UPDATE user_id=' + str(user_id)
    return sql


def replace_user_official():
    sql = 'REPLACE INTO bili_official(user_id,role,title,bili_official.desc,update_time) values (%s,%s,%s,%s,now())'
    return sql


def replace_uv_count():
    sql = 'REPLACE INTO bili_uv_count(tid,count,name,user_id)values(%s,%s,%s,%s)'
    return sql


def delete_detect_user(mid):
    sql = 'delete FROM bili_detect WHERE detect_id = ' + str(mid) + ' AND detect_type = 0'
    return sql

######################################
def insert_video_info():
    sql = 'INSERT INTO bili_video(video_id,tid,tname,video_title,video_profile,create_time,video_desc,video_view,video_favorite,coins,video_share,video_like,reply,dynamic,video_author,author_mid,last_update)' \
          'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
    return sql

def insert_video_bvid():
    sql = 'INSERT INTO bili_video_bvid(video_id,video_bvid) values (%s,%s)'


# 检查上上次用户视频数
def query_yesterday_user_video_count(mid):
    sql = 'Select video_count from bili_uploader WHERE user_id = ' + str(mid) + ' Order By last_update DESC limit 1,1'
    return sql


# 新建需要更新的视频列表 
def insert_detect_video():
    sql = 'INSERT INTO bili_detect(detect_id,detect_type,have_detect,max_detect,update_time,create_time)values(%s,1,1,7,now(),now()) '
    return sql


# 遍历需要更新的视频列表
def query_update_video_list():
    sql = 'SELECT  detect_id from bili_detect where have_detect<max_detect'
    return sql


# 对已经更新过的视频检测数+1
def update_video_detect_time(aid):
    sql = 'update bili_detect set have_detect=have_detect+1 where detect_id = ' + str(aid) + ' and detect_type=1'
    return sql


def update_complete_video_detect(aid):
    sql = 'update bili_detect set have_detect=max_detect where detect_id = ' + str(aid) + ' and detect_type=1'
    return sql
