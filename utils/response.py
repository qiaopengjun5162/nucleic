"""
@Project  : nucleic
@Author   : QiaoPengjun
@Time     : 2023/3/29 17:59
@Software : PyCharm
@File     : response.py
"""
from typing import List
from pydantic import BaseModel


# 用于响应分页数据的数据模型
class PageResponse(BaseModel):
    count: int  # 总记录数
    list: List  # 数据列表
