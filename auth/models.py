"""
@Project  : nucleic
@Author   : QiaoPengjun
@Time     : 2023/3/28 23:56
@Software : PyCharm
@File     : models.py
"""
from sqlalchemy import Column, String, Integer

from app.database import Base


class UserInDB(Base):  # 定义数据库模型
    __tablename__ = 'auth_user'  # 数据库中的表名
    id = Column('id', Integer, autoincrement=True, primary_key=True, doc='ID')
    username = Column('username', String(50))
    hashed_password = Column('hashed_password', String(64))
