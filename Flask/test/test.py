from Flask.item import global_val as gl
from Flask.spider import spider


def make_test():
    gl.set_value('CURRENT_USER_NUM', 10086)


# SUCCESS
def user_init():
    spider.init_parse_data()


# 第一日测试成功
# 第二日测试成功
# 第三日测试成功
def user_update():
    spider.update_parse_user()


# 第一日测试成功
# 第二日第一部分测试完成
# 第三日测试成功
def update_video():
    spider.update_video()


if __name__ == '__main__':
    gl._init()
    print("开始测试")
    # user_init()
    # user_update()
    update_video()
    print("结束测试")
