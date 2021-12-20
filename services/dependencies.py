from fastapi import Cookie, Depends
from typing import Optional
from services.jwt_token import decode_access_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def cookie_token(access_token: Optional[str] = Cookie(None)):
    return decode_access_token(access_token)
