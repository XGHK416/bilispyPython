# 对数据库进行操作
import pymysql


class Db(object):
    cursor = None
    db = None

    def start_sql_engine(self):
        self.db = pymysql.connect(host='39.106.228.42', user='Myself', password='hongzi123', db='Myself')
        self.cursor = self.db.cursor()

    def insert_or_update(self, item, sql):
        try:
            # print(sql)
            self.cursor.execute(sql, item)
            self.db.commit()
        except Exception as exc:
            print(exc)
            self.db.rollback()
            print("error")
            self.db.close()

    def select(self, sql):
        try:
            # print(sql)
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as exc:
            print(exc)
            self.db.rollback()
            print("error")
            self.db.close()

    def close_db(self):
        self.db.close()
