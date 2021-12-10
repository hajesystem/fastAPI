from fastapi import FastAPI, status
import uvicorn
# 라우터 import
from routers import basic

app = FastAPI(title="Python Backend", description="Fast API", version="0.0.1")

# routers
app.include_router(basic.router)


@app.get('/', status_code=status.HTTP_200_OK)
def root():
    return {'message': 'welcome FastAPI'}


if __name__ == '__main__':
    # uvicorn.run(app, host='0.0.0.0', port=3100)
    # reload=True : debug mode 활성화. 실서비스에서 제거한다.
    uvicorn.run('main:app', host='0.0.0.0', port=3100, reload=True)
