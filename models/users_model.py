from enum import unique

from models import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class UsersModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(32), unique=True)
    name = Column(String(32))


class InfoModel(Base):
    __tablename__ = 'info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(80), unique=True)
    phone = (Column(String(80), unique=True))
    address = Column(String(80))
