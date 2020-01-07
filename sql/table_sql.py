# 返回数据库语句


def user_info():
    return 'INSERT INTO user_info(mid,"name",birthday,face,"level",sex,vip) values(%d,%s,%s,%d,%s,%s,%s)ON DUPLICATE KEY UPDATE id=values(id)'

