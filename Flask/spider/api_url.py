def return_user_follow(start, limit, mid):
    return 'https://api.bilibili.com/x/relation/followings?vmid=' + str(mid) + '&pn=' + str(start) + '&ps=' + str(
        limit) + '&order=desc&jsonp=jsonp'


def return_user_info(mid):
    return 'https://api.bilibili.com/x/space/acc/info?mid=' + str(mid) + '&jsonp=jsonp'


def return_user_fans(start, limit, mid):
    return 'https://api.bilibili.com/x/relation/followers?vmid=' + str(mid) + '&pn=' + str(start) + '&ps=' + str(
        limit) + '&order=desc&jsonp=jsonp'


def return_user_follower_following(mid):
    return 'https://api.bilibili.com/x/relation/stat?vmid=' + str(mid) + '&jsonp=jsonp'


def return_video_info(aid):
    return 'https://api.bilibili.com/x/web-interface/view?aid=' + str(aid)


def return_user_video_count(mid, num):
    if num is not None:
        return 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=' + str(
            mid) + '&pagesize=' + str(num)
    else:
        return 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=' + str(
            mid) + '&pagesize=1'
