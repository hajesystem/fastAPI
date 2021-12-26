from typing import Text
from sqlalchemy.sql.sqltypes import Date
from models import Base
from sqlalchemy import Column, String, Integer, Date, Text
from sqlalchemy.orm import relationship


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(32), unique=True)
    password = Column(String(255))


class InfoModel(Base):
    __tablename__ = 'info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80))
    email = Column(String(80), unique=True)
    phone = Column(String(80), unique=True)


class ToDoModel(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    titile = Column(String(80))
    descript = Column(Text)
    user_id = Column(Integer)
