# 返回数据库语句


def user_info(user_id):
    sql = 'INSERT INTO bili_user(user_id,nick_name,profile,sex,level,sign,silence,vip,birthday,video_count,follower,following,last_update) ' \
          'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now()) '
    if user_id is not None:
        sql = sql + 'ON DUPLICATE KEY UPDATE user_id=' + str(user_id)
    return sql


def user_official():
    sql = 'REPLACE INTO bili_official(user_id,role,title,bili_official.desc) values (%s,%s,%s,%s)'
    return sql


def uv_count():
    sql = 'REPLACE INTO bili_uv_count(tid,count,name,user_id)values(%s,%s,%s,%s)'
    return sql


######################################
def video_info():
    sql = 'INSERT INTO bili_video(video_id,tid,video_title,video_profile,create_time,video_desc,video_view,video_favorite,coins,video_share,video_like,reply,dynamic)' \
          'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    return sql


# 检查昨日用户视频数
def check_update_video(mid):
    sql = 'SELECT video_count from bili_user where to_days(now())-to_days(last_update)=1 and user_id =' + str(mid)
    return sql


# 新建需要更新的视频列表
def add_update_video():
    sql = 'INSERT INTO bili_video_detect_list(video,update_time)values(%s,now()) '
    return sql


# 遍历需要更新的视频列表
def query_update_video_list():
    sql = 'SELECT  video_id from bili_video_detect_list where have_detect<max_detect'
    return sql


# 对已经更新过的视频检测数+1
def complete_detect(aid):
    sql = 'update bili_video_detect_list set have_detect=have_detect+1 where video_id = ' + str(aid)
