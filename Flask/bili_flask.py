# app.py
import copy
import datetime
import logging
from flask import Flask, render_template

from flask_apscheduler import APScheduler
from Flask.item import global_val as gl
from Flask.spider import spider
from Flask.util import enum


class Config(object):
    SCHEDULER_API_ENABLED = True


scheduler = APScheduler()

gl._init()

app = Flask(__name__, template_folder="./template")


#######################################################
# 初始化爬虫用户
@scheduler.task('date', id='init_parse_data', run_date=datetime.datetime(2020, 1, 29, 12, 00, 0))
def init_spider_user():
    try:
        app.logger.debug('开始init_parse_data')
        gl.set_value('current_task', enum.TaskList.init_parse_data.value)
        gl.set_value('status', enum.Status.Continue.value)
        start = datetime.datetime.now()
        gl.set_value('start_time', start)

        spider.init_parse_data()

        end = datetime.datetime.now()
        runtime = start - end
        gl._init()
        app.logger.debug('runtime:' + str(runtime))
    except Exception as exc:
        app.logger.error(exc)
        gl.set_value('status', enum.Status.Error.value)
        scheduler.pause_job('init_parse_data')


# 更新用户
@scheduler.task('cron', id='update_spider_user', start_date='2020-02-4', day_of_week='*', hour='4',
                misfire_grace_time=900)
def update_spider_user():
    try:
        app.logger.debug('开始update_spider_user')
        gl.set_value('current_task', enum.TaskList.update_spider_user.value)
        gl.set_value('status', enum.Status.Continue.value)
        start = datetime.datetime.now()
        gl.set_value('start_time', start)

        spider.update_parse_user()

        end = datetime.datetime.now()
        runtime = start - end
        gl._init()
        app.logger.debug('runtime:' + str(runtime))
    except Exception as exc:
        app.logger.error(exc)
        gl.set_value('status', enum.Status.Error.value)
        scheduler.pause_job('update_spider_user')


# 更新视频
@scheduler.task('cron', id='update_video', start_date='2020-02-4', day_of_week='*', hour='12',
                misfire_grace_time=900)
def update_video():
    try:
        app.logger.debug('开始update_video')
        gl.set_value('current_task', enum.TaskList.update_video.value)
        gl.set_value('status', enum.Status.Continue.value)
        start = datetime.datetime.now()
        gl.set_value('start_time', start)

        spider.update_video()

        end = datetime.datetime.now()
        runtime = start - end
        gl._init()
        app.logger.debug('runtime:' + str(runtime))
    except Exception as exc:
        app.logger.error(exc)
        gl.set_value('status', enum.Status.Error.value)
        scheduler.pause_job('update_video')


#########################################################
@app.route("/get_detect_info")
def get_detect_info():
    end_time = datetime.datetime.now()
    start_time = gl.get_value('start_time')
    result = copy.copy(gl.return_dict())
    result['start_time'] = start_time.__str__()
    result['have_time'] = (start_time-end_time).__str__()
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
