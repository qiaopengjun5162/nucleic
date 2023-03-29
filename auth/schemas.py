"""
@Project  : nucleic
@Author   : QiaoPengjun
@Time     : 2023/3/29 12:50
@Software : PyCharm
@File     : schemas.py
"""
from os import access
from typing import Optional

from powerline.segments.common.env import username
from pydantic import BaseModel


class Token(BaseModel):  # 定义Token的响应模型
    access_token: str
    token_type: str


class UserBase(BaseModel):  # 定义用户模型基类
    id: Optional[int]
    username: str


class UserCreate(UserBase):  # 定义创建用户的请求模型
    password: str


class User(UserBase):  # 定义返回用户信息的响应模型
    class Config:
        orm_mode = True
