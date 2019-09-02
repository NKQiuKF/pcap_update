from connect import engine, session, BaseModel, init_db, drop_db
from sqlalchemy import Column, ForeignKey, or_
from sqlalchemy.types import String, Integer, String, DateTime
from datetime import datetime
from station import Station

class Sensor(BaseModel):
    __tablename__='sensor'
    id=Column(Integer, primary_key=True)
    name=Column(String(80), unique=True, nullable=False)
    number=Column(String(80), unique=True, nullable=False)
    ip=Column(String(80))
    mac=Column(String(80), unique=True)
    stationId=Column(Integer, ForeignKey('station.id'))
    time=Column(DateTime)
    def __init__(self, name, number, ip, mac, stationId, time):
        self.name=name
        self.number=number
        self.ip=ip
        self.mac=mac
        self.stationId=stationId
        self.time=time

    def __repr__(self):
        return '<sensor: %r %r>' % (self.id, self.name)

    @staticmethod
    def check(name, number, ip, mac, stationId):
        '''
        :param name:
        :param number:
        :param stationId:
        :return:{1:'success', 2:'name repeat', 3:'number repeat', 4:'mac repeat', 5:'station id dose not exist'}
        '''
        ret=1
        query=session.query(Sensor)
        tmpSensor=query.filter(or_(Sensor.name==name, Sensor.number==number, Sensor.mac==mac)).all()
        for tSensor in tmpSensor:
            if(tSensor.name==name):
                ret=2
                return ret
            if(tSensor.number==number):
                ret=3
                return ret
            if(tSensor.mac==mac):
                ret=4
                return ret

        stationQuery=session.query(Station)
        tmpStation=stationQuery.filter_by(id=stationId).first()
        if(tmpStation==None):
            ret=5
            return ret
        return ret

    @staticmethod
    def add(name, number, ip, mac, stationId):
        '''
        1: success
        2: username repeat
        '''
        ret=1
        ret=Sensor.check(name, number, ip, mac, stationId)
        if(ret!=1):
            return ret

        curSensor=Sensor(name,number, ip, mac, stationId, datetime.now())
        session.add(curSensor)
        session.commit()
        return ret
init_db()