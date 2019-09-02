from user import User
from station import Station
from sensor import Sensor
from eqp import Eqp
from auth import Auth

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime


DB_CONNECT_STRING = 'mysql+mysqldb://root:mysql123@localhost/mnt2?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=False)

DB_Session = sessionmaker(bind=engine)
session = DB_Session()

BaseModel = declarative_base()


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


init_db()
