# 用户相关对象
# 请务必加上返回元组的方法return_tup，以便插入数据库


class VideoInfo(object):
    video_id = 0
    tid = 0
    video_title = '未知'
    video_profile = None
    create_time = 0
    video_desc = ''
    video_view = 0
    video_favorite = 0
    coins = 0
    video_share = 0
    video_like = 0
    reply = 0
    dynamic = ''
    video_author = ''
    author_mid = 0

    def __init__(self, video_id, tid, video_title, video_profile, create_time, video_desc, video_view, video_favorite,
                 coins, video_share, video_like,
                 reply, dynamic,
                 video_author, author_mid):
        self.author_mid = author_mid
        self.video_author = video_author
        self.dynamic = dynamic
        self.replay = reply
        self.video_like = video_like
        self.video_share = video_share
        self.coins = coins
        self.video_favorite = video_favorite
        self.video_view = video_view
        self.video_desc = video_desc
        self.create_time = create_time
        self.video_profile = video_profile
        self.video_title = video_title
        self.tid = tid
        self.video_id = video_id

    def return_tup(self):
        return (self.video_id, self.tid, self.video_title,
                self.video_profile, self.create_time, self.video_desc,
                self.video_view, self.video_favorite,
                self.coins, self.video_share,
                self.video_like, self.reply,
                self.dynamic,
                self.video_author, self.author_mid)
