# 유효성 검사 라우터
from fastapi import APIRouter, status
from schemas.validation_schema import ValidationModel
from sqlalchemy import text
from models import db_session

router = APIRouter(prefix='/validation', tags=['Validation'])


@router.post('/', status_code=status.HTTP_200_OK)
def validation(validation_data: ValidationModel):
    sql = 'SELECT * FROM  `%s` WHERE `%s`="%s"' % (
        validation_data.table, validation_data.column, validation_data.item)
    result = db_session.execute(text(sql)).first()
    # print(result)
    if result:
        return {'msg': '사용중 입니다.'}
    return {'msg': '사용할 수 있습니다.'}
