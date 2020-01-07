# 对数据库进行操作
import pymysql


class Db(object):
    cursor = None
    db = None

    def start_sql_engine(self):
        self.db = pymysql.connect(host='120.78.136.84', user='android', password='Android-123', db='android')
        self.cursor = self.db.cursor()

    def insert(self, item, sql):
        try:
            self.cursor.execute(sql, item.return_tup())
            self.db.commit()
        except Exception as exc:
            print(exc)
            self.db.rollback()
            print("error")

    def close_db(self):
        self.db.close()
