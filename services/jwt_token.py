import jwt
from fastapi import HTTPException, status, Depends, Request
from datetime import datetime, timedelta

import config
import sys
from fastapi.security.utils import get_authorization_scheme_param

from services.oauth2_cookie import OAuth2PasswordBearerWithCookie

# Adds higher directory to python modules path. config.py를 가져오기위한 설정
sys.path.append('..')

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl='/auth/create-token')


def encode_access_token(user):
    payload = {
        'exp': datetime.utcnow() + timedelta(seconds=config.ACCESS_TOKEN_TIME),
        'iat': datetime.utcnow(),
        'scope': 'access_token',
        'user': user
    }
    return jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)


def encode_refresh_token(user):
    payload = {
        'exp': datetime.utcnow() + timedelta(seconds=config.REFRESH_TOKEN_TIME),
        'iat': datetime.utcnow(),
        'scope': 'refresh_token',
        'user': user
    }
    return jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)


def refresh_token(request: Request):
    try:
        authorization: str = request.cookies.get('refresh_token')
        scheme, param = get_authorization_scheme_param(authorization)
        payload = jwt.decode(param, config.SECRET_KEY,
                             algorithms=[config.ALGORITHM])
        if(payload['scope'] != 'refresh_token'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scopes for token')
        print(payload)
        refresh_user = payload['user']
        new_access_token = encode_access_token(refresh_user)
        return new_access_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Refresh token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')


def get_current_user_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, config.SECRET_KEY,
                             algorithms=[config.ALGORITHM])
        current_user = payload['user']
        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid access token')
        elif(payload['scope'] != 'access_token'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scopes for token')
        return current_user
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Access token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid access token')
