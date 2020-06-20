# app.py
import copy
import datetime
import logging
from flask import Flask, render_template, request
import traceback

from Flask.predict import predict
from flask_apscheduler import APScheduler
from Flask.item import global_val as gl
from Flask.spider import spider
from Flask.util import enum
from Flask.dataUpdate import data_rank

FLASK_START_SUN = datetime.datetime.now()


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
        gl._init()
        app.logger.debug('开始init_parse_data')
        gl.set_value('current_task', enum.TaskList.init_parse_data.value)
        gl.set_value('status', enum.Status.Continue.value)
        start = datetime.datetime.now()
        gl.set_value('start_time', start)

        spider.init_parse_data()

        end = datetime.datetime.now()
        runtime = start - end
        app.logger.debug('runtime:' + str(runtime.seconds))
    except Exception as exc:
        app.logger.error(traceback.format_exc())
        gl.set_value('status', enum.Status.Error.value)
        scheduler.pause_job('init_parse_data')


# 更新用户
@scheduler.task('cron', id='update_spider_user', start_date='2020-02-4', day_of_week='*', hour='3', minute='10',
                misfire_grace_time=900)
def update_spider_user():
    try:
        # gl._init()
        app.logger.debug('开始update_spider_user')
        gl.set_value('current_task', enum.TaskList.update_spider_user.value)
        gl.set_value('status', enum.Status.Continue.value)
        start = datetime.datetime.now()
        gl.set_value('start_time', start)

        spider.update_parse_user()

        end = datetime.datetime.now()
        runtime = start - end
        app.logger.debug('runtime:' + str(runtime.seconds))
    except Exception as exc:
        app.logger.error(traceback.format_exc())
        gl.set_value('status', enum.Status.Error.value)
        scheduler.pause_job('update_spider_user')


# 更新视频
@scheduler.task('cron', id='update_video', start_date='2020-02-4', day_of_week='*', hour='12', minute='40',
                misfire_grace_time=900)
def update_video():
    try:
        # gl._init()
        app.logger.debug('开始update_video')
        gl.set_value('current_task', enum.TaskList.update_video.value)
        gl.set_value('status', enum.Status.Continue.value)
        start = datetime.datetime.now()
        gl.set_value('start_time', start)

        spider.update_video()

        end = datetime.datetime.now()
        runtime = start - end
        app.logger.debug('runtime:' + str(runtime.seconds))
    except Exception as exc:
        app.logger.error(traceback.format_exc())
        gl.set_value('status', enum.Status.Error.value)
        scheduler.pause_job('update_video')


# 更新排名
@scheduler.task('cron', id='update_rank', start_date='2020-02-4', day_of_week='*', hour='0',
                misfire_grace_time=900)
def update_rank():
    try:
        # gl._init()
        app.logger.debug('开始update_rank')
        gl.set_value('current_task', 'update_rank')
        gl.set_value('status', enum.Status.Continue.value)
        start = datetime.datetime.now()
        gl.set_value('start_time', start)

        spider.rank_update()

        end = datetime.datetime.now()
        runtime = start - end
        app.logger.debug('runtime:' + str(runtime.seconds))
    except Exception as exc:
        app.logger.error(traceback.format_exc())
        gl.set_value('status', enum.Status.Error.value)
        scheduler.pause_job('update_rank')


#########################################################
@app.route("/get_detect_info")
def get_detect_info():
    end_time = datetime.datetime.now()
    start_time = gl.get_value('start_time')
    result = copy.copy(gl.return_dict())
    result['start_time'] = start_time.__str__()
    result['have_time'] = (start_time - end_time).__str__()
    return str(result)


@app.route("/give_base_info")
def give_base_info():
    result = {}
    run_time = str(datetime.datetime.now() - FLASK_START_SUN).split(':')
    result['run_time_second'] = run_time
    result['total_video'] = gl.get_value('total_video')
    result['total_uploader'] = gl.get_value('total_user')
    result['today_video'] = gl.get_value('current_video')
    return str(result.__str__())


@app.route("/predict_count")
def predict_count():
    mid = request.args.get("mid")
    result={}
    result['num'] = predict.predict_count(mid)
    return str(result.__str__())


@app.route("/predict_status")
def predict_status():
    mid = request.args.get("mid")
    tid = request.args.get("tid")
    result = predict.predict_status(mid, tid)
    return str(result.__str__())


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
