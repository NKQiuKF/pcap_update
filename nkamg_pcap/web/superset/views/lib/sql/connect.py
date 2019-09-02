# coding=utf-8
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#your_path = os.path.path('.')
file_path = os.path.dirname(os.path.abspath(__file__))
your_db = file_path[:-7]+'antimal_db.sqlite'
DB_CONNECT_STRING = 'sqlite:///{your_db}'.format(your_db=your_db)
engine = create_engine(DB_CONNECT_STRING, echo=False)

DB_Session = sessionmaker(bind=engine)
session = DB_Session()

BaseModel = declarative_base()


def init_db():
    BaseModel.metadata.create_all(engine)

def drop_db():
    BaseModel.metadata.drop_all(engine)
