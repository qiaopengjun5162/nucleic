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
    db = SessionLocal()  # 创建数据库会话
    cnt = db.query(func.count(UserInDB.username)).scalar()  # 查询数据库中的账号数量
    if cnt == 0:  # 当数据库中无账号时
        user = UserInDB(username=AUTH_INIT_USER, hashed_password=get_password_hash(AUTH_INIT_PASSWORD))  # 创建初始账号
        db.add(user)
        db.commit()  # 提交数据
    db.close()  # 关闭会话


# 获取单个用户
def get_user(db: Session, username: str):
    return db.query(UserInDB).filter(UserInDB.username == username).first()


# 创建一个用户
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)  # 第一步，计算密码的哈希值
    db_user = UserInDB(username=user.username, hashed_password=hashed_password)
    db.add(db_user)  # 第二步，将实例添加到会话
    db.commit()  # 第三步，提交会话
    db.refresh(db_user)  # 第四步，刷新实例，用于获取数据或者生成数据库中的ID
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
async def get_current_user(
        token: str = Depends(AUTH_SCHEMA),  # 依赖项，身份认证
        db: Session = Depends(get_db)):  # 依赖项，数据库连接
    invalid_exception = HTTPException(  # 自定义异常
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的用户凭据",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:  # 开始捕获错误
        username: str = extract_token(token)  # 从token中解析出账号
        if username is None:  # 检测账号是否有效
            raise invalid_exception
    except JWTError:  # 出现解析异常时
        raise invalid_exception  # 抛出自定义异常
    user = get_user(db, username=username)  # 根据账号从数据库中查找用户信息
    if user is None:  # 未找到用户信息时
        raise invalid_exception  # 抛出自定义异常
    return user
