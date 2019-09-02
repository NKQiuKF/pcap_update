from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base




DB_CONNECT_STRING = 'sqlite:////home/nkamg/nkamg-7.24/web/antimal_db.sqlite'
engine = create_engine(DB_CONNECT_STRING, echo=False)

DB_Session=sessionmaker(bind=engine)
session=DB_Session()

BaseModel = declarative_base()
def init_db():
    BaseModel.metadata.create_all(engine)
def drop_db():
    BaseModel.metadata.drop_all(engine)
