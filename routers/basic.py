from fastapi import APIRouter, status
from typing import Optional
from pydantic import BaseModel
from schemas.basic import Basic

router = APIRouter(prefix="/basic", tags=["Basic"])


@router.get('/', status_code=status.HTTP_200_OK)
# parameter 사용
def basic(title: str = 'BASIC', is_login: bool = True, name: Optional[str] = None):
    if is_login:
        return {'data': f'{title} {name} 로그인을 환영합니다.'}
    else:
        return {'data': f'{title} 로그인 정보가 없습니다.'}


@router.get('/{id}', status_code=status.HTTP_200_OK)
# url parameter 사용
def url(id: int):
    return {'id': id}


@router.get('/{id}/comments', status_code=status.HTTP_200_OK)
def comment(id, limit=10):
    # fetch data
    return {'data': {'1', '2'}}


@router.post('/post', status_code=status.HTTP_201_CREATED)
# post 요청으로 변수를 가져온다.
def create(basic: Basic):
    return {'title': basic.title, 'descript': basic.descript, 'option': basic.option}
