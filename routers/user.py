# ORM을 이용한 FastAPI 구성
from typing import List
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

# Pydantic 모델과 같은 Object를 수신하고 JSON 호환 버전을 반환
from fastapi.encoders import jsonable_encoder

# 데이터베이스
from sqlalchemy import insert, select, delete, update
from models.user_model import UserModel
from models import db_session

# parameter schema
from schemas.user_schema import UserIn, UserOut


router = APIRouter(prefix='/user', tags=['User'])

# response_model ==> 반환할 결과물을 정의한 스카마 형태로 반환


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserOut])
def get_all():
    try:
        user_all = select(UserModel)
        # db_session.execute(user_all).all() ==> [{"Model": {...},{...} }}] 배열 반환
        result = db_session.execute(user_all).scalars().all()
        return result
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.get('/{id}')
def get(id: int):
    try:
        user = select(UserModel).where(UserModel.id == id)
        # db_session.execute(user).one() ==> {...}
        # db_session.execute(user).first() ==> {'DbModel':{...}}
        # db_session.execute(user).scalar() ==> null 또는 {}
        result = db_session.execute(user).scalar()
        if not result:
            # raise 강제로 error 발생시킨다.
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='user id : {id} not found')
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.post('/')
def create(user: UserIn):
    try:
        add_user = insert(UserModel).values(
            user=user.user, password=user.password)
        db_session.execute(add_user)
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
        user = select(UserModel).where(UserModel.id == id)
        result = db_session.execute(user).scalar()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                                'msg': f'{id} not found'})
        del_user = delete(UserModel).where(UserModel.id == id)
        db_session.execute(del_user)
        db_session.commit()
        db_session.close()
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

    except SQLAlchemyError as error:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.put('/{id}')
def edit(id: int, user: UserIn):
    try:
        user = select(UserModel).where(UserModel.id == id)
        result = db_session.execute(user).scalar()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                                'msg': f'{id} not found'})
        update_user = update(UserModel).where(
            UserModel.id == id).values(user=user.user, password=user.password)
        db_session.execute(update_user)
        db_session.commit()
        db_session.close()
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user))

    except SQLAlchemyError as error:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))