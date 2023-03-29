"""
@Project  : nucleic
@Author   : QiaoPengjun
@Time     : 2023/3/28 23:55
@Software : PyCharm
@File     : services.py
"""
from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db, SessionLocal
from app.settings import AUTH_SCHEMA, AUTH_INIT_USER, AUTH_INIT_PASSWORD
from utils.password import get_password_hash, verify_password
from utils.token import extract_token
from .models import UserInDB
from .schemas import UserCreate


# 创建初始管理员账号
def init_admin_user():
    db = SessionLocal()
    cnt = db.query(func.count(UserInDB.username)).scalar()
    if cnt == 0:
        user = UserInDB(username=AUTH_INIT_USER, hashed_password=get_password_hash(AUTH_INIT_PASSWORD))
        db.add(user)
        db.commit()
    db.close()


# 获取单个用户
def get_user(db: Session, username: str):
    return db.query(UserInDB).filter(UserInDB.username == username).first()


# 创建一个用户
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)  # 计算密码的哈希值
    db_user = UserInDB(username=user.username, hashed_password=hashed_password)
    db.add(db_user)  # 将实例添加到会话
    db.commit()  # 提交会话
    db.refresh(db_user)  # 刷新实例，用于获取数据或者生成数据库中的ID
    return db_user


# 验证用户和密码
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return True


# 获取当前用户信息的依赖函数
async def get_current_user(token: str = Depends(AUTH_SCHEMA), db: Session = Depends(get_db)):
    invalid_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的用户凭据",
                                      headers={"WWW-Authenticate": "Bearer"})
    try:
        username: str = extract_token(token)
        if username is None:
            raise invalid_exception
    except JWTError:
        raise invalid_exception
    user = get_user(db, username=username)
    if user is None:
        raise invalid_exception
    return user
