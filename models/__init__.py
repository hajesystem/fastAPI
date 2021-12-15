# 데이터베이스 접속설정
import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
# scoped_session은 프로퍼티를 가지고 있으며, 세션의 자동완성기능을 사용할 수 있도록한다..

conn = config.MYSQL_CONN

# 연결설정 create_engine()
engine = create_engine(conn, echo=True, convert_unicode=True, future=True)

# 세션 생성
db_session = scoped_session(sessionmaker(
    bind=engine, autocommit=False, autoflush=False))
# 베이스 선언
Base = declarative_base()

# query_property() : select 할 속성을 Base에 미리 담아둔다
# Base.query = db_session.query_property()
