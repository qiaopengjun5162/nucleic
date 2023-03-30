"""
@Project  : nucleic
@Author   : QiaoPengjun
@Time     : 2023/3/29 11:23
@Software : PyCharm
@File     : router.py
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from auth.services import AUTH_SCHEMA
from utils.response import PageResponse
from .schemas import Person
from .services import save_person, get_person, get_params

route = APIRouter(tags=['预约'])


@route.post('/submit', response_model=Person)
async def submit(data: Person, db: Session = Depends(get_db)):  # 预约登记
    return save_person(db, data)  # 保存从前端传递过来的新的预约信息，并响应返回


@route.get('/get', response_model=Person, dependencies=[Depends(AUTH_SCHEMA)])
async def get(zjhm: str, db: Session = Depends(get_db)):  # 查询指定条件的预约信息
    return get_person(db, zjhm)  # 响应返回查询的预约信息
