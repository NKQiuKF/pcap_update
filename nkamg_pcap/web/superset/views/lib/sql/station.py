from connect import engine, session, BaseModel, init_db, drop_db
from sqlalchemy import Column, or_
from sqlalchemy.types import String, Integer, DateTime
from datetime import datetime


class Station(BaseModel):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    number = Column(String(80), unique=True, nullable=False)
    supervisor = Column(String(80))
    phone = Column(String(80))
    time = Column(DateTime)
    valid = Column(Integer, default=1)

    def __init__(self, name, number, supervisor, phone, time):
        self.name = name
        self.number = number
        self.supervisor = supervisor
        self.phone = phone
        self.time = time

    def __repr__(self):
        return '<station: %d %r>' % (self.id, self.name)

    @staticmethod
    def check(name, number):
        '''
        1: 'success',
        2: 'name repeat'
        3: 'number repeat'
        4: 'name is empty'
        5: 'number is empty'
        '''
        ret = 1
        if(name == ''):
            ret = 4
            return ret
        if(number == ''):
            ret = 5
            return ret

        query = session.query(Station)
        tmpStation = query.filter(
            or_(Station.name == name, Station.number == number), Station.valid == 1).all()
        for tStation in tmpStation:
            if(tStation.name == name):
                ret = 2
                return ret
            if(tStation.number == number):
                ret = 3
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
        ret = 1
        if(name == ''):
            ret = 4
            return ret
        if(number == ''):
            ret = 5
            return ret
        ret = Station.check(name, number)
        if(ret != 1):
            return ret
        curStation = Station(name, number, supervisor, phone, datetime.now())
        session.add(curStation)
        session.commit()
        return ret

    @staticmethod
    def eqpNum():
        ret = {}
        ret['data'] = []
        allData = session.execute(
            'select station_name ,count(1) as nums from (select station.name as station_name from station join sensor on station.id=sensor.stationId join eqp on sensor.id=eqp.sensorId) as total group by station_name order by nums desc limit 5;').fetchall()
        for tmpData in allData:
            tmp = {}
            tmp['name'] = tmpData.station_name
            tmp['count'] = tmpData.nums
            ret['data'].append(tmp)
        return ret

    @staticmethod
    def select(inData):
        ret = {}
        ret['status'] = 1
        ret['data'] = []
        ret['pureData'] = []
        query = session.query(Station)
        allStation = None

        if('id' in inData):
            allStation = query.filter(
                Station.id == inData['id'],
                Station.valid == 1).all()
        elif('number' in inData):
            allStation = query.filter(
                Station.number == inData['number'],
                Station.valid == 1).all()
        elif('name' in inData):
            allStation = query.filter(
                Station.name == inData['name'],
                Station.valid == 1).all()
        else:
            allStation = query.filter(Station.valid == 1).all()

        for tmpData in allStation:
            tmp = {}
            tmp['id'] = tmpData.id
            tmp['name'] = tmpData.name
            tmp['number'] = tmpData.number
            tmp['supervisor'] = tmpData.supervisor
            tmp['phone'] = tmpData.phone
            tmp['time'] = tmpData.time
            ret['data'].append(tmp)
            ret['pureData'].append(tmpData)
        return ret

    @staticmethod
    def updateStation(inData):
        '''
        :param: inData
        :return: {1:'success', 2:'name repeat', 3:'permission denied', 4:'param wrong', 5:'number repeat'}
        '''
        from user import User
        if(('UserId' in inData) and ('StationId' in inData) and (('Name' in inData) or ('Number' in inData) or ('Supervisor' in inData) or ('Phone' in inData))):
            updateUserLevel = session.query(
                User.level).filter(
                User.id == inData['UserId'],
                User.valid == 1).first()
            if(updateUserLevel is None or int(updateUserLevel[0] != 0)):
                return 3
            else:
                if('Name' in inData and inData['Name'] != ''):
                    tmpStation = session.query(Station).filter(
                        Station.name == inData['Name'], Station.valid == 1).first()
                    if(tmpStation is not None):
                        return 2
                    session.query(Station).filter(Station.id == inData['StationId'], Station.valid == 1).update(
                        {'name': inData['Name'], 'time': datetime.now()})
                if('Number' in inData and inData['Number'] != ''):
                    tmpStation = session.query(Station).filter(
                        Station.number == inData['Number'], Station.valid == 1).first()
                    if(tmpStation is not None):
                        return 5
                    session.query(Station).filter(Station.id == inData['StationId'], Station.valid == 1).update(
                        {'number': inData['Number'], 'time': datetime.now()})
                if('Supervisor' in inData and inData['Supervisor'] != ''):
                    session.query(Station).filter(Station.id == inData['StationId'], Station.valid == 1).update(
                        {'supervisor': inData['Supervisor'], 'time': datetime.now()})
                if('Phone' in inData and inData['Phone'] != ''):
                    session.query(Station).filter(Station.id == inData['StationId'], Station.valid == 1).update(
                        {'phone': inData['Phone'], 'time': datetime.now()})
                session.commit()
                return 1
        else:
            return 4

    @staticmethod
    def delStation(inData):
        '''
        :param: inData
        :return: {1:'success', 2:'failed', 3:'permission denied', 4:'param wrong'}
        '''
        from user import User
        from sensor import Sensor
        if(('UserId' in inData) and ('StationId' in inData)):
            updateUserLevel = session.query(
                User.level).filter(
                User.id == inData['UserId'],
                User.valid == 1).first()
            if(updateUserLevel is None or int(updateUserLevel[0] != 0)):
                return 3
            else:
                session.query(Station).filter(Station.id == inData['StationId'], Station.valid == 1).update(
                    {'valid': 0, 'time': datetime.now()})
                delSensorId = session.query(
                    Sensor.id).filter(
                    Sensor.stationId == inData['StationId'],
                    Sensor.valid == 1).all()
                for sensorId in delSensorId:
                    Sensor.delSensor(
                        {'UserId': inData['UserId'], 'SensorId': int(sensorId[0])})
                session.commit()
                return 1
        else:
            return 4

    @staticmethod
    def update_station2(inData):
        '''
        :param inData:
        :return: {0:'errror', 1:'success', 2:'no this id', 3:'iData has no key id', 4:'name input is none', 5:'number is none', 6:'supervisor is none'},
        7:'phone is none'}
        '''
        ret = 1
        if('id' not in inData):
            ret = 3
            return ret
        query = session.query(Station)
        tmpStation = query.filter(Station.id == inData['id']).first()
        if(tmpStation is None):
            ret = 2
            return ret
        if('name' in inData):
            if(inData['name'] != ''):
                tmpStation.name = inData['name']
            else:
                ret = 4
        if('number' in inData):
            if(inData['number'] != ''):
                tmpStation.number = inData['number']
            else:
                ret = 5
        if('supervisor' in inData):
            tmpStation.supervisor = inData['supervisor']
            # if(inData['supervisor']!=''):
            #     tmpStation.supervisor=inData['supervisor']
            # else:
            #     ret=6
        if('phone' in inData):
            tmpStation.phone = inData['phone']
            # if(inData['phone']!=''):
            #     tmpStation.phone=inData['phone']
            # else:
            #     ret=7

        session.commit()
        return ret

    @staticmethod
    def delete_station2(inData):
        '''
        :param inData:
        :return:{
            2:'there is no id in inData',
            3:'there is no such id'
        }
        '''
        ret = 0
        if('id' not in inData):
            ret = 2
            return ret

        query = session.query(Station)
        tmpStation = query.filter(Station.id == inData['id']).first()
        if(tmpStation is None):
            ret = 3
            return ret
        else:
            from sensor import Sensor
            tmpAllSensor = Sensor.select({'stationId': tmpStation.id})
            for tmpSensor in tmpAllSensor['pureData']:
                tmpSensor.stationId = 0
            session.delete(tmpStation)
            session.commit()
            ret = 1
            return ret

    init_db()
