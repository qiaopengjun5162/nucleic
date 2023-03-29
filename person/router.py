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
from .services import save_person, list_person, get_person, get_params
