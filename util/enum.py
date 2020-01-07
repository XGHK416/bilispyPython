import enum


class UserLevel(enum.Enum):
    LEVEL0 = 'level0'
    LEVEL1 = 'level1'
    LEVEL2 = 'level2'
    LEVEL3 = 'level3'
    LEVEL4 = 'level4'
    LEVEL5 = 'level5'
    LEVEL6 = 'level6'


class UserVip(enum.Enum):
    VISITOR = '游客'
    NORMAL = '普通会员'
    BIG_VIP = '大会员'
