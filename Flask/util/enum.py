import enum


class UserLevel(enum.Enum):
    Level0 = 0
    Level1 = 1
    Level2 = 2
    Level3 = 3
    Level4 = 4
    Level5 = 5
    Level6 = 6


class UserVip(enum.Enum):
    VISITOR = 0
    BIG_VIP = 1
    YEARS_BIG_VIP = 2


class UserOfficial(enum.Enum):
    NO_AUTHS = 0
    PERSONAL_AUTHS_1 = 1
    PERSONAL_AUTHS_2 = 2
    OFFICIAL_AUTHS = 3


class TaskList(enum.Enum):
    no_task = '没有任务'
    init_parse_data = '初始化爬虫'
    update_spider_user = '更新用户资料'
    update_video = '更新视频资料'


class Status(enum.Enum):
    Continue = '执行中'
    Error = '执行错误'
    Wait = '等待执行'

if __name__ == '__main__':
    print(UserLevel('level0').name)