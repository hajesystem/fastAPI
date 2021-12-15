from typing import Optional
import jwt
from .. import config
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Cookie

secret = config.SECRET_KEY
algorithms = config.ALGORITHM


def encode_access_token(user):
    payload = {
        'exp': datetime.utcnow()+timedelta(seconds=config.ACCESS_TOKEN_TIME),
        'iat': datetime.utcnow,  # 토큰 생성시간
        'scope': 'access_token',
        'user': user
    }
    # 단축형으로 사용함. payload = payload
    return jwt.encode(payload, secret, algorithms)


def encode_refresh_token(user):
    payload = {
        'exp': datetime.utcnow() + timedelta(seconds=config.REFRESH_TOKEN_TIME),
        'iat': datetime.utcnow(),
        'scope': 'refresh_token',
        'user': user
    }
    return jwt.encode(payload, secret, algorithms)


def decode_access_token(token):
    try:
        payload = jwt.decode(token, secret, algorithms)
        if (payload['scope'] != 'access_token'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        return payload['user']
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Access token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid access token')


def refresh_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, secret, algorithms)
        if(payload['scope'] != 'refresh_token'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        refresh_user = payload['user']
        new_access_token = encode_access_token(refresh_user)
        return new_access_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Refresh token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')


def cookie_token(access_token: Optional[str] = Cookie(None)):
    return decode_access_token(access_token)
