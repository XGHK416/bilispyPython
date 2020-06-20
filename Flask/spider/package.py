# 对对象进行封装

from Flask.item import user
from Flask.item import video
from Flask.util import enum
import time


def package_user_info(user_info, user_ff, video_count):
    # print(json)
    user_info = user_info.get('data')
    user_ff = user_ff.get('data')
    # print(json.get('coins'))
    return user.UserInfo(
        user_id=user_info.get('mid'),
        nick_name=user_info.get('name'),
        profile=user_info.get('face'),
        sex=user_info.get('sex'),
        level=enum.UserLevel(user_info.get('level')).name,
        sign=user_info.get('sign'),
        silence=user_info.get('silence'),
        vip=enum.UserVip(user_info.get('vip').get('type')).name,
        birthday=user_info.get('birthday'),
        follower=user_ff.get('follower'),
        following=user_ff.get('following'),
        video_count=video_count
    )


def package_video_info(video_info):
    video_data = video_info.get('data')
    create_time = video_data.get('pubdate')
    timeArray = time.localtime(create_time)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return video.VideoInfo(
        video_id=video_data.get('aid'),
        tid=video_data.get('tid'),
        tname=video_data.get('tname'),
        video_title=video_data.get('title'),
        video_profile=video_data.get('pic'),
        create_time=current_time,
        video_desc=video_data.get('desc'),
        video_view=video_data.get('stat').get('view'),
        video_favorite=video_data.get('stat').get('favorite'),
        coins=video_data.get('stat').get('coin'),
        video_share=video_data.get('stat').get('share'),
        video_like=video_data.get('stat').get('like'),
        reply=video_data.get('stat').get('reply'),
        dynamic=video_data.get('dynamic'),
        video_author=video_data.get('owner').get('name'),
        author_mid=video_data.get('owner').get('mid'),
    )


def package_video_bvid(video_info):
    video_data = video_info.get('data')
    return video.VideoBvid(
        video_id=video_data.get('aid'),
        video_bvid=video_data.get('bvid'),
    )


def package_user_official(user_info):
    return user.UserOfficial(
        user_id=user_info.get('data').get('mid'),
        role=user_info.get('data').get('official').get('role'),
        title=user_info.get('data').get('official').get('title'),
        desc=user_info.get('data').get('official').get('desc'),
    )


def package_video_count(user_video_category, mid):
    return user.UserVideoCount(
        user_id=mid,
        tid=user_video_category.get('tid'),
        count=user_video_category.get('count'),
        name=user_video_category.get('name'),
    )
