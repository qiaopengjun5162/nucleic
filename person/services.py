"""
@Project  : nucleic
@Author   : QiaoPengjun
@Time     : 2023/3/29 17:32
@Software : PyCharm
@File     : services.py
"""
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import PersonInDB
from .schemas import Person


# 定义依赖函数
async def get_params(
        xm: Optional[str] = None,
        lxdh: Optional[str] = None,
        jzdz: Optional[str] = None,
        page: Optional[int] = 1,
        size: Optional[int] = 10):
    return {'xm': xm, 'lxdh': lxdh, 'jzdz': jzdz, 'page': page, 'size': size}


# 保存预约信息
def save_person(db: Session, data: Person):
    dbdata = PersonInDB(**data.dict())
    db.add(dbdata)
    db.commit()
    db.refresh(dbdata)
    return dbdata


def get_person(db: Session, zjhm):
    data = db.query(PersonInDB).filter(PersonInDB.zjhm == zjhm).first()
    return data
