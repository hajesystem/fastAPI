# DATABASE CREATE TABLE
from models import db_model, engine

db_model.Base.metadata.create_all(bind=engine)
