# 用户相关对象
# 请务必加上返回元组的方法return_tup，以便插入数据库
import datetime


class UserInfo(object):
    user_id = 00000
    nick_name = None
    profile = ''
    sex = None
    level = 0
    sign = ''
    silence = ''
    vip = ''
    birthday = None
    video_count = 0
    follower = 0
    following = 0

    def __init__(self, user_id, nick_name, profile, sex, level, sign, silence, vip, birthday, video_count, follower,
                 following):
        self.video_count = video_count
        if sign != '':
            self.sign = sign
        self.following = following
        self.follower = follower
        self.birthday = birthday
        self.vip = vip
        self.silence = silence
        self.level = level
        self.sex = sex
        self.profile = profile
        self.nick_name = nick_name
        self.user_id = user_id

    def return_tup(self):
        return [int(self.user_id), self.nick_name, self.profile, self.sex, self.level, self.sign, int(self.silence),
                self.vip,
                self.birthday, self.video_count,
                int(self.follower), int(self.following)]


class UserOfficial(object):
    user_id = None
    role = None
    title = None
    desc = None

    def __init__(self, user_id, role, title, desc):
        self.desc = desc
        self.title = title
        self.role = role
        self.user_id = user_id

    def return_tup(self):
        return [self.user_id, self.role, self.title, self.desc]


class UserVideoCount(object):
    tid = 0
    count = 0
    name = ''
    user_id = 0

    def __init__(self, tid, count, name, user_id):
        self.name = name
        self.count = count
        self.tid = tid
        self.user_id = user_id

    def return_tup(self):
        return [self.tid, self.count, self.name, self.user_id]


# class UserVideo(object):
#     video_id = None
#     tid = 0
#     video_title = None
#     video_profile = None
#     create_time = None
#     video_desc = None
#     video_view = None
#     video_favorite = None
#     coins = 0
#     video_share = None
#     video_like = None
#
#     def __init__(self, video_id, tid, video_title, video_profile, create_time, video_desc, video_view, video_favorite,
#                  coins, video_share, video_like):
#         self.video_like = video_like
#         self.video_share = video_share
#         self.coins = coins
#         self.video_favorite = video_favorite
#         self.video_view = video_view
#         self.video_desc = video_desc
#         self.create_time = create_time
#         self.video_profile = video_profile
#         self.video_title = video_title
#         self.tid = tid
#         self.video_id = video_id
#
#     def return_tup(self):
#         return (self.video_id, self.tid, self.video_title, self.video_profile, self.create_time, self.video_desc,
#                 self.video_view,
#                 self.video_favorite, self.coins, self.video_share, self.video_like)


if __name__ == '__main__':
    temple = UserOfficial(1, 2, 3, 4)
    print(temple.return_tup())
