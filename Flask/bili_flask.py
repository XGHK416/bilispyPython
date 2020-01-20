# app.py
import datetime
from threading import Lock

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder="./template")
socketio = SocketIO(app)

_thread = None
lock = Lock()


@app.route("/")
def index():
    return render_template("index.html")


# used as callback
def background_task():
    # your trigger event
    while True:
        current_datetime = str(datetime.datetime.now())


#         # current_datetime = "datetime is : " + current_datetime
#         #
#         # # emit to your named event
#         # socketio.emit("server_response", {"data": current_datetime})
#         # socketio.sleep(10)


@socketio.on("connect", namespace="/wechat")
def connect():
    print('connect')


@socketio.on("message", namespace="/wechat")
def handle_message():
    print("message")
    while True:
        print("112")
        socketio.emit("response", {"data": 1}, namespace="/wechat")
        socketio.sleep(5)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=6789, debug=True)
