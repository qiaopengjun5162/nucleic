"""
@Project  : nucleic
@Author   : QiaoPengjun
@Time     : 2023/3/28 23:21
@Software : PyCharm
@File     : database.py
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.settings import *

engine = create_engine(  # 创建数据库引擎实例
    f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # 定义数据库会话类

Base = declarative_base()  # 定义数据库模型基类


def get_db():  # 定义数据库依赖函数
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 根据 Sqlalchemy 的数据库模型定义，将数据库模型生成数据库中的表结构
def generate_tables():
    Base.metadata.create_all(bind=engine)
