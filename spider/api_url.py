def return_user_follow(start, limit, mid):
    return 'https://api.bilibili.com/x/relation/followings?vmid=' + mid + '&pn=' + start + '&ps=' + limit + '&order=desc&jsonp=jsonp'


def return_user_info(mid):
    return 'https://api.bilibili.com/x/space/acc/info?mid=' + str(mid) + '&jsonp=jsonp'


def return_user_fans(start, limit, mid):
    return 'https://api.bilibili.com/x/relation/followers?vmid=' + mid + '&pn=' + start + '&ps=' + limit + '&order=desc&jsonp=jsonp'

