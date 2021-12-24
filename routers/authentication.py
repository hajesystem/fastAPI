from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy.exc import SQLAlchemyError
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from models.user_model import UserModel
from models import db_session
from services.jwt_token import refresh_token, encode_access_token, encode_refresh_token
from schemas.user_schema import UserIn, UserOut

# password hashing
import bcrypt

# Pydantic 모델과 같은 Object를 수신하고 JSON 호환 버전을 반환
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post("/create-token", status_code=status.HTTP_200_OK, response_model=UserOut)
# inputtype ==> { username: name, password: password }
def login(response: Response, user: OAuth2PasswordRequestForm = Depends()):
    try:
        sql = select(UserModel).where(UserModel.user == user.username)
        check_user: UserIn = db_session.execute(sql).scalar()
        # if not 조건 : 먼저 사용하는 이유는 최소 연산을 하기 위하여 false 상태부터 구현한다.
        if not check_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f'{user.username} not found.')
        check_password = bcrypt.checkpw(
            user.password.encode('utf-8'), check_user.password.encode('utf-8'))  # True or False
        if not check_password:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Password is incorrect.')
        access_token = encode_access_token(user.username)
        refresh_token = encode_refresh_token(user.username)
        response.set_cookie(key="access_token",
                            value=f"Bearer {access_token}", httponly=True)
        response.set_cookie(key="refresh_token",
                            value=f"Bearer {refresh_token}", httponly=True)
        return check_user

    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.get('/remove-token', status_code=status.HTTP_200_OK)
def logout(response: Response):
    try:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return "token removed"

    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='error')


@router.get("/refresh-token")
def refresh_token(response: Response, new_access_token: str = Depends(refresh_token)):
    response.set_cookie(key="access_token",
                        value=f"Bearer {new_access_token}", httponly=True)
    return 'access_token refresh'
