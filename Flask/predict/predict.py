from Flask.sql.do_sql import Db
import datetime
from sklearn.linear_model import LinearRegression as LR
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import pandas as pd

db = Db()


def predict_count(mid):
    sql = "SELECT count( * ) count,MONTH ( create_time ) month FROM ( SELECT * FROM bili_video WHERE video_id IN ( SELECT video_id FROM bili_video WHERE bili_video.author_mid = " + mid + " GROUP BY video_id ) ) AS v WHERE NOT EXISTS ( SELECT * FROM bili_video AS b WHERE v.video_id = b.video_id AND v.last_update < b.last_update ) GROUP BY MONTH ( create_time ) ORDER BY MONTH ( create_time ) ASC;"
    db.start_sql_engine()
    count = list(db.select(sql))
    count.pop()
    db.close_db()

    X = []
    y = []
    tags = ['月份']
    today_month = datetime.datetime.now().month
    for index, item in enumerate(count):
        X.append(item[1])
        y.append(item[0])

    table = pd.DataFrame(X)
    table.columns = tags

    next_ = predict_count_method(table, y, today_month)

    return int(next_[0])


def predict_status(mid, tname):
    sql = "SELECT video_view,video_like,coins,video_favorite,tid FROM(SELECT * FROM bili_video WHERE bili_video.video_id IN (SELECT sc.video_id FROM( SELECT video_id FROM bili_video_rank WHERE uploader_id = " + mid + " GROUP BY video_id ORDER BY rank DESC ) AS sc ) ORDER BY bili_video.last_update DESC ) r WHERE NOT EXISTS ( SELECT * FROM bili_video AS b WHERE r.video_id = b.video_id AND r.last_update < b.last_update ) ORDER BY r.create_time ASC"
    db.start_sql_engine()
    status = list(db.select(sql))
    db.close_db()

    view_y = []
    like_y = []
    coins_y = []
    favorite_y = []
    status_x = []
    count = 1
    tags = ["tname"]
    for index, item in enumerate(status):
        count = count + 1
        status_x.append([item[4]])
        view_y.append(item[0])
        like_y.append(item[1])
        coins_y.append(item[2])
        favorite_y.append(item[3])

    table = pd.DataFrame(status_x)
    table.columns = tags

    view = predict_status_method(table, view_y, tname)
    like = predict_status_method(table, like_y, tname)
    coins = predict_status_method(table, coins_y, tname)
    favorite = predict_status_method(table, favorite_y, tname)

    result = {}
    result['view'] = int(view[0])
    result['like'] = int(like[0])
    result['coins'] = int(coins[0])
    result['favorite'] = int(favorite[0])

    # print(table.head())

    # print(count)
    # print(status_x)
    # print(view_y, like_y, coins_y, favorite_y)
    return result


def predict_status_method(X, y, tname):
    Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, y, test_size=0.3, random_state=100)
    for i in [Xtrain, Xtest]:
        i.index = range(i.shape[0])

    reg = LR().fit(Xtrain, Ytrain)
    need_predict = pd.DataFrame([[tname]])
    yhat = reg.predict(need_predict)
    return yhat

def predict_count_method(X, y, month):
    Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, y, test_size=0.2, random_state=100)
    for i in [Xtrain, Xtest]:
        i.index = range(i.shape[0])

    reg = LR().fit(Xtrain, Ytrain)
    need_predict = pd.DataFrame([[month]])
    yhat = reg.predict(need_predict)
    return yhat