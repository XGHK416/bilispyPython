# 对对象进行封装

from item import user


def package_user_info(json):
    # print(json)
    json = json.get('data')
    # print(json.get('coins'))
    return user.UserInfo(
        mid=json.get('mid'),
        name=json.get('name'),
        sex=json.get('sex'),
        face=json.get('face'),
        level=json.get('level'),
        birthday=json.get('birthday'),
        vip=json.get('vip'),
    )
