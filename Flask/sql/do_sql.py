# 对数据库进行操作
import logging

import pymysql
from DBUtils.PooledDB import PooledDB, SharedDBConnection


class Db(object):
    cursor = None
    conn = None

    def __new__(cls, *args, **kw):
        '''
        启用单例模式
        :param args:
        :param kw:
        :return:
        '''
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.POOL = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,
            # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0,
            # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host='39.106.228.42',
            port=3306,
            user='Myself',
            password='hongzi123',
            database='Myself',
            charset='utf8'
        )

    def start_sql_engine(self):
        self.conn = self.POOL.connection()
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.Cursor)
        # //////////////
        # self.db = pymysql.connect(host='39.106.228.42', user='Myself', password='hongzi123', db='Myself')
        # self.cursor = self.db.cursor()

    def insert_or_update(self, item, sql):
        try:
            # print(sql)
            self.cursor.execute(sql, item)
            self.conn.commit()
            return True
        except Exception as exc:
            logging.warning(exc)
            return False
            # self.db.close()

    def select(self, sql):
        try:
            # print(sql)
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as exc:
            logging.error(exc)
            self.conn.close()

    def close_db(self):
        self.cursor.close()
        self.conn.close()
        # self.db.close()
