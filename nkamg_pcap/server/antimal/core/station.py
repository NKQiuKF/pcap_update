from connect import engine, session, BaseModel, init_db, drop_db
from sqlalchemy import Column, or_
from sqlalchemy.types import String, Integer, DateTime
from datetime import datetime


class Station(BaseModel):
    __tablename__='station'
    id=Column(Integer, primary_key=True)
    name=Column(String(80), unique=True, nullable=False)
    number=Column(String(80), unique=True, nullable=False)
    supervisor=Column(String(80))
    phone=Column(String(80))
    time=Column(DateTime)
    def __init__(self, name, number, supervisor, phone, time):
        self.name=name
        self.number=number
        self.supervisor=supervisor
        self.phone=phone
        self.time=time
    def __repr__(self):
        return '<station: %d %r>' % (self.id, self.name)

    @staticmethod
    def check(name, number):
        '''
        1: success
        2: name repeat
        3: number repeat
        '''
        ret=1
        query=session.query(Station)
        tmpStation=query.filter(or_(Station.name==name, Station.number==number)).all()
        for tStation in tmpStation:
            if(tStation.name==name):
                ret=2
                return ret
            if(tStation.number==number):
                ret=3
                return ret

        return ret
    @staticmethod
    def add(name, number, supervisor, phone):
        '''
        :param name:
        :param number:
        :param supervisor:
        :param phont:
        :return: {1:'success', 2:'name repeat', 3:'number repeat', 4:'name is empty', 5:'number is empty'}
        '''
        ret=1
        if(name==''):
            ret=4
            return ret
        if(number==''):
            ret=5
            return ret
        ret=Station.check(name, number)
        if(ret!=1):
            return ret
        curStation=Station(name, number, supervisor, phone, datetime.now())
        session.add(curStation)
        session.commit()
        return ret

    init_db()