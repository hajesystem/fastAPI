# ORM을 이용한 FastAPI 구성
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

# Pydantic 모델과 같은 Object를 수신하고 JSON 호환 버전을 반환
from fastapi.encoders import jsonable_encoder

# 데이터베이스
from models.users_model import UsersModel
from sqlalchemy import insert, select, delete, update
from models import db_session

# parameter schema
from schemas.users_schema import UsersSchema


router = APIRouter(prefix='/user', tags=['User'])


@router.get('/', status_code=status.HTTP_200_OK)
def get_all():
    sql = select(UsersModel)
    # db_session.execute(sql).all() ==> [{},{}] 배열 반환
    # result = db_session.execute(sql).all()
    result = db_session.execute(sql).all()
    return result


@router.get('/{id}')
def get(id: int):
    try:
        select_sql = select(UsersModel).where(UsersModel.id == id)
        # db_session.execute(sql).one() ==> {}
        # db_session.execute(sql).first() ==> {'DbModel':{}}
        # db_session.execute(sql).scalar() ==> null 또는 {}
        result = db_session.execute(select_sql).scalar()
        if not result:
            # raise 강제로 error 발생시킨다.
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='user id : {id} not found')
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.post('/')
def create(user: UsersSchema):
    try:
        insert_sql = insert(UsersModel).values(user=user.user, name=user.name)
        db_session.execute(insert_sql)
        db_session.commit()
        db_session.close()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(user))

    except SQLAlchemyError as error:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.delete('/{id}')
def remove(id: int):
    try:
        select_sql = select(UsersModel).where(UsersModel.id == id)
        result = db_session.execute(select_sql).scalar()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                                'msg': f'{id} not found'})
        delete_sql = delete(UsersModel).where(UsersModel.id == id)
        db_session.execute(delete_sql)
        db_session.commit()
        db_session.close()
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

    except SQLAlchemyError as error:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.put('/{id}')
def edit(id: int, user: UsersSchema):
    try:
        select_sql = select(UsersModel).where(UsersModel.id == id)
        result = db_session.execute(select_sql).scalar()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                                'msg': f'{id} not found'})
        update_sql = update(UsersModel).where(
            UsersModel.id == id).values(user=user.user, name=user.name)
        db_session.execute(update_sql)
        db_session.commit()
        db_session.close()
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user))

    except SQLAlchemyError as error:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))
