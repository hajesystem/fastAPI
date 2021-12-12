# ORM을 이용한 FastAPI 구성

from fastapi import APIRouter, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
# 데이터베이스
from models.users_model import UsersModel
from sqlalchemy import insert, select
from models import db_session
# parameter schema
from schemas.users_schema import UsersSchema


router = APIRouter(prefix='/user', tags=['User'])


@router.get('/', status_code=status.HTTP_200_OK)
def get_all():
    sql = select(UsersModel)
    result = db_session.execute(sql).all()
    return result


@router.get('/{id}', status_code=status.HTTP_200_OK)
def get(id: str):
    sql = select(UsersModel).where(UsersModel.id == id)
    result = db_session.execute(sql).all()
    return result


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(user: UsersSchema):
    try:
        sql = insert(UsersModel).values(user=user.user, name=user.name)
        db_session.execute(sql)
        db_session.commit()
        return 'Done'
    except SQLAlchemyError as error:
        db_session.rollback()
        return error
