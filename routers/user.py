# ORM을 이용한 FastAPI 구성
from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# password hashing
import bcrypt

# Pydantic 모델과 같은 Object를 수신하고 JSON 호환 버전을 반환
from fastapi.encoders import jsonable_encoder

# 데이터베이스
from sqlalchemy import insert, select, delete, update
from models.db_model import UserModel
from models import get_db

# parameter schema
from schemas.user_schema import UserIn, UserOut
from services.jwt_token import get_current_user_token


router = APIRouter(prefix='/user', tags=['User'])

# response_model ==> 반환할 결과물을 정의한 스카마 형태로 반환


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserOut])
def get_all(current_user=Depends(get_current_user_token), db: Session = Depends(get_db)):
    try:
        select_all = select(UserModel)
        result = db.execute(select_all).scalars().all()
        # return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))
        return result
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.get('/{id}',  response_model=UserOut)
def get(id: int, current_user=Depends(get_current_user_token), db: Session = Depends(get_db)):
    try:
        print(id)
        select_user = select(UserModel).where(UserModel.id == id)
        # db.execute(select_user).one() ==> {...}
        # db.execute(select_user).first() ==> {'DbModel':{...}}
        # db.execute(select_user).scalar() ==> null 또는 {}
        result = db.execute(select_user).scalar()
        if not result:
            # raise 강제로 error 발생시킨다.
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
        return result

    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.post('/')
def create(user: UserIn, db: Session = Depends(get_db)):
    try:
        hash_password = (bcrypt.hashpw(user.password.encode(
            'UTF-8'), bcrypt.gensalt(12))).decode('utf-8')
        add_user = insert(UserModel).values(
            user=user.user, password=hash_password)
        db.execute(add_user)
        db.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(user))

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.delete('/{id}')
def remove(id: int, current_user=Depends(get_current_user_token), db: Session = Depends(get_db)):
    try:
        select_user = select(UserModel).where(UserModel.id == id)
        result = db.execute(select_user).scalar()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                                'msg': f'{id} not found'})
        del_user = delete(UserModel).where(UserModel.id == id)
        db.execute(del_user)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.put('/{id}')
def edit(id: int, user: UserIn, current_user=Depends(get_current_user_token), db: Session = Depends(get_db)):
    try:
        select_user = select(UserModel).where(UserModel.id == id)
        result = db.execute(select_user).scalar()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                                'msg': f'{id} not found'})
        update_user = update(UserModel).where(
            UserModel.id == id).values(user=user.user, password=user.password)
        db.execute(update_user)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user))

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))
