from Flask.sql import data_rank_sql as update
import pymysql

db = pymysql.connect(
    host='39.106.228.42',
    user='Myself',
    password='hongzi123',
    db='Myself',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = db.cursor()


def select(sql):
    global db, cursor
    try:
        # print(sql)
        cursor.execute(sql)
        res = cursor.fetchall()
        return res
    except Exception as exc:
        db.rollback()
        db.close()


def insert(item, sql):
    global db, cursor
    try:
        # print(sql)
        cursor.execute(sql, item)
        db.commit()
        return True
    except Exception as exc:
        print(exc)
        db.rollback()
        return False
        # self.db.close()


def video_rank_update():
    global db
    result = select(update.query_video())
    print("total" + str(len(result)))
    for item in result:
        view = item['video_view']
        favorite = item['video_favorite']
        coins = item['coins']
        like = item['video_like']

        video_id = item['video_id']
        uploader_id = item['author_mid']
        section = item['tname']
        score = view * 0.8 + (coins * 0.3 + like * 0.3 + favorite * 0.3) * 100 * 0.2
        flag = insert((video_id, score, section, uploader_id), update.insert_video_rank())

    db.close()


def uploader_rank_update():
    global db
    result = select(update.query_uploader())
    for item in result:
        uploader_id = item['user_id']
        section_tuple = select(update.query_uploader_video_section(uploader_id))
        if len(section_tuple) != 0:
            section = section_tuple[0]['name']
            if section is None:
                section = '未分区'
        else:
            section = '未分区'
        # print(section)

        video_score_tuple = select(update.query_uploader_video_score(uploader_id))
        if len(video_score_tuple) != 0:
            video_score = video_score_tuple[0]['video_score']
            if video_score is None:
                video_score = 0
        else:
            video_score = 0
        uploader_score = item['follower'] * 0.5
        score = int(int(video_score) * 10000 * 0.5 + int(uploader_score) * 1000)
        flag = insert((uploader_id, score, section), update.insert_uploader_rank())
    db.close()


def rank():
    video_rank_update()
    uploader_rank_update()
