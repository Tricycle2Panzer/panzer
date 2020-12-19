from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
import psycopg2

class db():
    def __init__(self):
        engine = create_engine('postgresql://postgres:40960032@localhost:5432/bookstore')#确定好服务器地址再修改
        Base = declarative_base()
        DBSession = sessionmaker(bind=engine)
        self.conn = DBSession()