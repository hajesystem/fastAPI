# login / logout 구현
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
from schemas.user_schema import UserIn


router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.get('/login', status_code=status.HTTP_200_OK)
def login(user: UserIn):
    try:
        return "login"
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.get('/logout', status_code=status.HTTP_200_OK)
def logout():
    try:
        return "logout"

    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))
