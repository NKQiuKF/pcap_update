from connect import engine, session, BaseModel, init_db, drop_db
from sqlalchemy import Column, ForeignKey, or_, func
from sqlalchemy.types import String, Integer, DateTime
from datetime import datetime
from sensor import Sensor
from user import User


class Auth(BaseModel):
    __tablename__ = 'auth'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('userv2.id'))
    sensorId = Column(Integer, ForeignKey('sensor.id'))
    time = Column(DateTime)
    valid = Column(Integer, default=1)

    def __init__(self, userId, sensorId, time):
        self.userId = userId
        self.sensorId = sensorId
        self.time = time

    def __repr__(self):
        return '<auth: %d %d %d>' % (self.id, self.userId, self.sensorId)

    @staticmethod
    def check(userId, sensorId):
        '''
        :param userId:
        :param sensorId:
        :return: {1:'success', 2:'userId not exist', 3:'sensorId not exist', 4:'authority exist'}
        '''
        ret = 1
        userQuery = session.query(User)
        tmpUser = userQuery.filter(User.id == userId).first()
        if(tmpUser is None):
            ret = 2
            return ret
        sensorQuery = session.query(Sensor)
        tmpSensor = sensorQuery.filter(Sensor.id == sensorId)
        if(tmpSensor is None):
            ret = 3
            return ret

        query = session.query(Auth)
        tmpAuth = query.filter(
            Auth.userId == userId,
            Auth.sensorId == sensorId).first()
        if(tmpAuth is not None):
            ret = 4
            return ret
        return ret

    @staticmethod
    def add(userId, sensorId):
        ret = 1
        ret = Auth.check(userId, sensorId)
        if(ret != 1):
            return ret
        curAuth = Auth(userId, sensorId, datetime.now())
        session.add(curAuth)
        session.commit()
        return ret

    @staticmethod
    def select(inData):
        ret = {}
        ret['status'] = 1
        ret['data'] = []
        ret['pureData'] = []
        query = session.query(Auth)
        allAuth = None

        if('id' in inData):
            allAuth = query.filter(Auth.id == inData['id']).all()
        elif('userId' in inData):
            allAuth = query.filter(Auth.userId == inData['usreId']).all()
        elif('sensorId' in inData):
            allAuth = query.filter(Auth.sensorId == inData['sensorId']).all()
        else:
            allAuth = query.filter().all()

        for tmpData in allAuth:
            tmp = {}
            tmp['id'] = tmpData.id
            tmp['userId'] = tmpData.userId
            tmp['sensorId'] = tmpData.sensorId
            ret['data'].append(tmp)
            ret['pureData'].append(tmpData)
        return ret

    @staticmethod
    def info(inData):
        from user import User
        from sensor import Sensor
        from station import Station
        pureData = Auth.select(inData)

        userInfo = {}
        sensorInfo = {}
        stationInfo = {}
        # print(pureData)

        for tmp in pureData['data']:
            t = tmp['sensorId']
            if(not(t in sensorInfo)):
                curSensor = Sensor.select({'id': t})
                sensorInfo[t] = curSensor
            tmp['sensorName'] = sensorInfo[t]['data'][0]['name']

            t = sensorInfo[t]['data'][0]['stationId']
            if(not(t in stationInfo)):
                curStation = Station.select({id: t})
                stationInfo[t] = curStation
            tmp['stationName'] = stationInfo[t]['data'][0]['name']

            t = tmp['userId']
            if(not(t in userInfo)):
                curUser = User.select({'id': t})
                userInfo[t] = curUser
            tmp['userName'] = userInfo[t]['data'][0]['username']

        return pureData

    @staticmethod
    def delAuth(inData):
        '''
        :param inData:
        :return:{1:'success', 2:'wrong param'}
        '''
        if(('UserId' in inData) or ('SensorId' in inData)):
            if(('UserId' in inData) and ('SensorId' in inData)):
                session.query(Auth).filter(
                    Auth.userId == inData['UserId'],
                    Auth.sensorId == inData['SensorId']).update(
                    {
                        'valid': 0,
                        'time': datetime.now()})
            elif('UserId' in inData):
                session.query(Auth).filter(Auth.userId == inData['UserId']).update(
                    {'valid': 0, 'time': datetime.now()})
            else:
                session.query(Auth).filter(Auth.sensorId == inData['SensorId']).update(
                    {'valid': 0, 'time': datetime.now()})
            session.commit()
        else:
            return 2
        return 1

    @staticmethod
    def delete_auth2(inData):
        '''
        :param inData:
        :return: {2:'there is no id', 3:'this is so such record'}
        '''
        ret = 1
        if('id' in inData):
            query = session.query(Auth)
            tmpAuth = query.filter(Auth.id == inData['id']).first()
            if(tmpAuth is not None):
                session.delete(tmpAuth)
                session.commit()
                ret = 1
            else:
                ret = 3

        else:
            ret = 2
        return ret


init_db()
