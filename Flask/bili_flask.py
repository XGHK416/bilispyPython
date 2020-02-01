# app.py
import datetime
import logging
from flask import Flask, render_template

from flask_apscheduler import APScheduler
from Flask.item import global_val as gl
from Flask.spider import spider


class Config(object):
    SCHEDULER_API_ENABLED = True


scheduler = APScheduler()

gl._init()
gl.set_zero('CURRENT_SPIDER_MID')
gl.set_zero('CURRENT_SPIDER_AID')
gl.set_value('STATE', 200)
gl.set_value('TOTAL_VIDEO_NUM', 0)
gl.set_value('TOTAL_USER_NUM', 0)
gl.set_value('CURRENT_VIDEO_NUM', 0)
gl.set_value('CURRENT_USER_NUM', 0)
gl.set_value('TASK_NAME', '--')
gl.set_value('INIT_MID', 3043120)

app = Flask(__name__, template_folder="./template")


#######################################################
# 初始化爬虫用户
@scheduler.task('date', id='init_parse_data', run_date=datetime.datetime(2020, 1, 29, 12, 00, 0))
def init_spider_user():
    try:
        app.logger.debug('开始init_parse_data')
        gl.set_value('TASK_NAME', '初始化爬取用户')
        start = datetime.datetime.now()
        spider.init_parse_data()
        end = datetime.datetime.now()
        runtime = start - end
        app.logger.debug('init_runtime:' + str(runtime))
        gl.set_value('TOTAL_USER_NUM', gl.get_value('CURRENT_USER_NUM'))
        gl.set_value('CURRENT_USER_NUM', 0)
        gl.set_value('TASK_NAME', 'complete')
    except Exception as exc:
        app.logger.error(exc)
        gl.set_value('STATE', 300)
        gl.set_value('CURRENT_USER_NUM', 0)
        gl.set_value('TASK_NAME', '--')
        scheduler.pause_job('init_parse_data')


# 更新用户
@scheduler.task('cron', id='update_spider_user', start_date='2020-02-1', day_of_week='*', hour='18',
                misfire_grace_time=900)
def update_spider_user():
    try:
        gl.set_value('TASK_NAME', '更新用户爬取')
        start = datetime.datetime.now()

        spider.update_parse_user()

        end = datetime.datetime.now()
        runtime = start - end
        app.logger.debug('init_runtime:' + str(runtime))

        gl.set_value('TASK_NAME', 'complete')
        gl.set_value('CURRENT_USER_NUM', 0)
    except Exception as exc:
        app.logger.error(exc)
        app.logger.error(gl.get_value('CURRENT_SPIDER_MID'))
        gl.set_value('TASK_NAME', '--')
        gl.set_value('CURRENT_USER_NUM', 0)
        gl.set_value('STATE', 300)
        scheduler.pause_job('update_spider_user')


# 更新视频
@scheduler.task('cron', id='update_video', start_date='2020-02-1', day_of_week='*', hour='12',
                misfire_grace_time=900)
def update_video():
    try:
        gl.set_value('TASK_NAME', '更新视频资源')
        start = datetime.datetime.now()

        spider.update_video()

        end = datetime.datetime.now()
        runtime = start - end
        app.logger.debug('init_runtime:' + str(runtime))

        gl.set_value('TASK_NAME', 'complete')
        gl.set_value('CURRENT_VIDEO_NUM', 0)
    except Exception as exc:
        app.logger.error(exc)
        app.logger.error(gl.get_value('CURRENT_SPIDER_AID'))
        gl.set_value('TASK_NAME', '--')
        gl.set_value('CURRENT_VIDEO_NUM', 0)
        gl.set_value('STATE', 300)
        scheduler.pause_job('update_video')


#########################################################
@app.route("/get_detect_info")
def get_detect_info():
    result = {}
    result['state'] = gl.get_value('STATE')
    result['scheduler_state'] = scheduler.state
    result['current_task'] = gl.get_value('TASK_NAME')
    result['current_user_num'] = gl.get_value('CURRENT_USER_NUM')
    result['current_video_num'] = gl.get_value('CURRENT_VIDEO_NUM')
    result['total_user_num'] = gl.get_value('TOTAL_USER_NUM')
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
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    app.config.from_object(Config())
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

if __name__ == "__main__":
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
