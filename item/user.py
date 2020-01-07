# 用户相关对象
# 请务必加上返回元组的方法return_tup，以便插入数据库


class UserInfo(object):
    mid = 00000
    name = None
    sex = '未知'
    face = None
    level = 0
    birthday = ''
    vip = ''

    def __init__(self, mid, name, sex, face, level, birthday, coins, vip):
        self.level = level
        self.birthday = birthday
        self.face = face
        self.sex = sex
        self.name = name
        self.vip = vip
        self.mid = mid

    def return_tup(self):
        return(self.mid,
               self.name,
               self.birthday,
               self.face,
               self.level,
               self.sex,
               self.vip)
