# DATABASE CREATE TABLE
from models import engine, user_model

user_model.Base.metadata.create_all(bind=engine)
