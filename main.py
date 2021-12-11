from fastapi import FastAPI, status
import uvicorn
# 라우터 import
from routers import basic
from routers import users
# DATABASE
from models import engine, users_model


description = """
Python Backend

## MD 파일 형식의 편집

일반서체 **볼드서체**.

* **Python** 
* API
"""

app = FastAPI(title="FastAPI", description=description, version="0.0.1")

# DATABASE CREATE TABLE
users_model.Base.metadata.create_all(engine)

# routers
app.include_router(basic.router)
app.include_router(users.router)


@app.get('/', tags=['Main'], status_code=status.HTTP_200_OK)
def root():
    return {'message': 'welcome FastAPI'}


if __name__ == '__main__':
    # uvicorn.run(app, host='0.0.0.0', port=3100)
    # reload=True : debug mode 활성화. 실서비스에서 제거한다.
    uvicorn.run('main:app', host='0.0.0.0', port=3100, reload=True)
