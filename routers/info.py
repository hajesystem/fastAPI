from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models import get_db
from models.db_model import InfoModel

from schemas.info_schema import InfoIn, InfoOut
from services.jwt_token import get_current_user_token

router = APIRouter(prefix='/info', tags=['UserInfo'])


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[InfoOut])
def get_all(current_user=Depends(get_current_user_token), db: Session = Depends(get_db)):
    try:
        select_all = select(InfoModel)
        # db.execute(select_all).all() ==> [{"Model": {...},{...} }}] 배열 반환
        result = db.execute(select_all).scalars().all()
        return result
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.post('/')
def create(info: InfoIn, current_user=Depends(get_current_user_token), db: Session = Depends(get_db)):
    try:
        add_info = insert(InfoModel).values(
            name=info.name, email=info.email, phone=info.phone, user_id=info.user_id)
        db.execute(add_info)
        db.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(info))

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.get('/{user_id}')
def get(user_id: int, current_user=Depends(get_current_user_token), db: Session = Depends(get_db)):
    try:
        select_user = select(InfoModel).where(InfoModel.user_id == user_id)
        result = db.execute(select_user).scalar()
        if not result:
            # raise 강제로 error 발생시킨다.
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f'{user_id} not found')
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.delete('/{id}')
def remove(id: int, current_user=Depends(get_current_user_token), db: Session = Depends(get_db)):
    try:
        select_user = select(InfoModel).where(InfoModel.id == id)
        result = db.execute(select_user).scalar()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                                'msg': f'{id} not found'})
        del_user = delete(InfoModel).where(InfoModel.id == id)
        db.execute(del_user)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))


@router.put('/{id}')
def edit(id: int, info: InfoIn, current_user=Depends(get_current_user_token), db: Session = Depends(get_db)):
    try:
        select_user = select(InfoModel).where(InfoModel.id == id)
        result = db.execute(select_user).scalar()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                                'msg': f'{id} not found'})
        update_user = update(InfoModel).where(
            InfoModel.id == id).values(name=info.name, email=info.email, phone=info.phone, user_id=info.user_id)
        db.execute(update_user)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(info))

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=jsonable_encoder(error))
