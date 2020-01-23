# app.py
import datetime
from spider import spider
from flask import Flask, render_template

from flask_apscheduler import APScheduler
from item import global_val as gl
from test import test


class Config(object):
    SCHEDULER_API_ENABLED = True


scheduler = APScheduler()
app = Flask(__name__, template_folder="./template")

# 测试
@scheduler.task('date', id='test_1', run_date=datetime.datetime(2020, 1, 23, 21, 56, 0),
                misfire_grace_time=900)
def test_1():
    print(gl.get_value('CURRENT_USER_NUM'))
#######################################################
# 初始化爬虫用户
@scheduler.task('date', id='init_parse_data', run_date=datetime.datetime(2020, 1, 30, 12, 0, 0),
                misfire_grace_time=900)
def init_spider_user():
    try:
        spider.init_parse_data()
        gl.set_value('ALL_USER_NUM', gl.get_value('CURRENT_USER_NUM'))
        gl.set_value('CURRENT_USER_NUM',0)
    except Exception as exc:
        print(exc)
        scheduler.pause_job('init_parse_data')


# 更新用户
@scheduler.task('cron', id='update_spider_user', start_date='2020-02-1', day_of_week=1, hour='12',
                misfire_grace_time=900)
def update_spider_user():
    try:
        spider.update_parse_user()

    except Exception as exc:
        print(exc)
        scheduler.pause_job('update_spider_user')


# 更新视频
@scheduler.task('cron', id='update_video', start_date='2020-02-1', day_of_week=0, hour='4',
                misfire_grace_time=900)
def update_video():
    try:
        spider.update_video()
    except Exception as exc:
        print(exc)
        scheduler.pause_job('update_video')


#########################################################
@app.route("/get_detect_info")
def get_detect_info():
    result = {}
    result['state'] = 200
    result['scheduler_state'] = scheduler.state
    result['current_task'] = gl.get_value('CURRENT_TASK')
    result['current_user_num'] = gl.get_value('CURRENT_USER_NUM')
    result['current_video_num'] = gl.get_value('CURRENT_VIDEO_NUM')
    return str(result)


@app.route("/")
def index():
    return render_template("detect.html")


# # used as callback
# def background_task():
#     # your trigger event
#     while True:
#         current_datetime = str(datetime.datetime.now())
#
#
# #         # current_datetime = "datetime is : " + current_datetime
# #         #
# #         # # emit to your named event
# #         # socketio.emit("server_response", {"data": current_datetime})
# #         # socketio.sleep(10)
# @socketio.on("connect", namespace="/bili_spider")
# def connect():
#     print('connect')


# 接受message请求
# @socketio.on("message", namespace="/bili_spider")
# def handle_message():
#     global CURRENT_USER_NUM
#     while True:
#         # 发送'response'请求
#         socketio.emit("response", {"data": CURRENT_USER_NUM}, namespace="/bili_spider")
#         socketio.sleep(5)
#

if __name__ == "__main__":
    gl._init()
    gl.set_value('CURRENT_USER_NUM', 0)
    gl.set_value('ALL_USER_NUM', 0)
    gl.set_value('CURRENT_VIDEO_NUM', 0)
    gl.set_value('NEW_ADD_VIDEO_NUM', 0)
    gl.set_value('CURRENT_TASK', '--')
    gl.set_value('INIT_MID', 3043120)

    app.config.from_object(Config())
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()
    app.run()
    # app.config.from_object(Config())
    #
    # socketio.run(app, host="0.0.0.0", port=6789, debug=True)
    # socketio.start_background_task(target=start_background())
