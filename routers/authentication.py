# login / logout 구현
from fastapi import APIRouter, status, Response, HTTPException
from pydantic import errors
from sqlalchemy.exc import SQLAlchemyError

# password hashing
import bcrypt

# Pydantic 모델과 같은 Object를 수신하고 JSON 호환 버전을 반환
from fastapi.encoders import jsonable_encoder

# 데이터베이스
from sqlalchemy import select
from models.user_model import UserModel
from models import db_session

# parameter schema
from schemas.user_schema import UserIn, UserOut
from services.jwt_token import encode_access_token, encode_refresh_token


router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post('/login', status_code=status.HTTP_200_OK, response_model=UserOut)
def login(user: UserIn, response: Response):
    try:
        sql = select(UserModel).where(UserModel.user == user.user)
        check_user: UserIn = db_session.execute(sql).scalar()
        # if not 조건 : 먼저 사용하는 이유는 최소 연산을 하기 위하여 false 상태부터 구현한다.
        if not check_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f'{user.user} not found.')
        check_password = bcrypt.checkpw(
            user.password.encode('utf-8'), check_user.password.encode('utf-8'))  # True or False
        if not check_password:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Password is incorrect.')
        else:
            access_token = encode_access_token(user.user)
            refresh_token = encode_refresh_token(user.user)
            response.set_cookie(key="access_token",
                                value=access_token, httponly=True)
            response.set_cookie(key="refresh_token",
                                value=refresh_token, httponly=True)
            return check_user

    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response):
    try:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return "logout"

    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='error')
