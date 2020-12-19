import logging
import os
# import sqlite3 as sqlite # del
from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

class Store:
    database: str

    def __init__(self, db_path):
        # self.database = os.path.join(db_path, "be.db")#修改成db文件中远程连接的数据库
        self.engine = create_engine('postgresql://postgres:40960032@127.0.0.1:5432/bookstore') #本地服务器
        self.init_tables()

    def init_tables(self):
        try:
            conn = self.get_db_conn()
            conn.execute(
                "CREATE TABLE IF NOT EXISTS users ("
                "user_id TEXT PRIMARY KEY, password TEXT NOT NULL, "
                "balance INTEGER NOT NULL, token TEXT, terminal TEXT);"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS user_store("
                "user_id TEXT, store_id TEXT , PRIMARY KEY(user_id, store_id));"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS store( "
                "store_id TEXT, book_id TEXT, book_info TEXT, stock_level INTEGER,"
                " PRIMARY KEY(store_id, book_id))"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS new_order( "
                "order_id TEXT PRIMARY KEY, user_id TEXT, store_id TEXT)"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS new_order_detail( "
                "order_id TEXT, book_id TEXT, count INTEGER, price INTEGER,  "
                "PRIMARY KEY(order_id, book_id))"
            )

            conn.commit()
        except IntegrityError as e:# 查sqlalchemy
            logging.error(e)
            conn.rollback()

    # def get_db_conn(self) -> sqlite.Connection:# 查sqlalchemy 中的操作，返回db中的数据库
    #     return sqlite.connect(self.database)
    def get_db_conn(self):
        self.Base = declarative_base()
        self.metadata = MetaData()
        self.DBSession = sessionmaker(bind=self.engine)
        self.conn = self.DBSession()
        return self.conn


database_instance: Store = None


def init_database(db_path):
    global database_instance
    database_instance = Store(db_path)


def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()# 要返回postgre
