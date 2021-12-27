from fastapi import FastAPI, status
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
# routers import
from routers import authentication, basic, user, info, validation

description = """
Python Backend

## MD 파일 형식의 편집

일반서체 **볼드서체**.

* **Python** 
* API
"""

app = FastAPI(title="FastAPI", description=description, version="0.0.1")


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATABASE CREATE TABLE ==> 외부 파일로 변경(별도로 실행) : python create_databases.py
# user_model.Base.metadata.create_all(engine)

# routers
app.include_router(authentication.router)
app.include_router(basic.router)
app.include_router(user.router)
app.include_router(info.router)
app.include_router(validation.router)


@app.get('/', tags=['Main'], status_code=status.HTTP_200_OK)
def root():
    return {'message': 'welcome FastAPI'}


if __name__ == '__main__':
    # uvicorn.run(app, host='0.0.0.0', port=3100)
    # reload=True : debug mode 활성화. 실서비스에서 제거한다.
    uvicorn.run('main:app', host='0.0.0.0', port=3100, reload=True)
