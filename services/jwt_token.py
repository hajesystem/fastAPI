import jwt
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import config
import sys

# Adds higher directory to python modules path. config.py를 가져오기위한 설정
sys.path.append("..")


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


def decode_access_token(token):
    try:
        payload = jwt.decode(token, config.SECRET_KEY,
                             algorithms=[config.ALGORITHM])
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
        payload = jwt.decode(refresh_token, config.SECRET_KEY,
                             algorithm=config.ALGORITHM)
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


# def cookie_token(access_token: Optional[str] = Cookie(None)):
#     return decode_access_token(access_token)
