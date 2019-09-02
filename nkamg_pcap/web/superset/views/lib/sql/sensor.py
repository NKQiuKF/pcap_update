from connect import engine, session, BaseModel, init_db, drop_db
from sqlalchemy import Column, ForeignKey, or_
from sqlalchemy.types import String, Integer, String, DateTime
from datetime import datetime
from station import Station
from user import User


class Sensor(BaseModel):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    number = Column(String(80), unique=True, nullable=False)
    ip = Column(String(80))
    mac = Column(String(80), unique=True)
    stationId = Column(Integer)
    time = Column(DateTime)
    valid = Column(Integer, default=1)

    def __init__(self, name, number, ip, mac, stationId, time):
        self.name = name
        self.number = number
        self.ip = ip
        self.mac = mac
        self.stationId = stationId
        self.time = time

    def __repr__(self):
        return '<sensor: %r %r>' % (self.id, self.name)

    @staticmethod
    def check(name, number, ip, mac, stationId):
        '''
        :param name:
        :param number:
        :param stationId:
        :return:{1:'success', 2:'name repeat', 3:'number repeat', 4:'mac repeat', 5:'station id dose not exist', 6:'sensor name is empty', 7:'sensor number is empty'
        8:'sensor ip is empty',
        9:'sensor mac is empty',
        }
        '''
        ret = 1
        if(name == ''):
            ret = 6
            return ret
        if(number == ''):
            ret = 7
            return ret

        if(mac == ''):
            ret = 9
            return ret

        if(ip == ''):
            ret = 8
            return ret

        query = session.query(Sensor)
        tmpSensor = query.filter(or_(Sensor.name == name,
                                     Sensor.number == number,
                                     Sensor.mac == mac),
                                 Sensor.valid == 1).all()
        for tSensor in tmpSensor:
            if(tSensor.name == name):
                ret = 2
                return ret
            if(tSensor.number == number):
                ret = 3
                return ret
            if(tSensor.mac == mac):
                ret = 4
                return ret

        stationQuery = session.query(Station)
        tmpStation = stationQuery.filter_by(id=stationId, valid=1).first()
        if(tmpStation is None):
            ret = 5
            return ret
        return ret

    @staticmethod
    def add(name, number, ip, mac, stationId):
        '''
        1: success
        2: username repeat
        '''
        ret = 1
        ret = Sensor.check(name, number, ip, mac, stationId)
        if(ret != 1):
            return ret

        curSensor = Sensor(name, number, ip, mac, stationId, datetime.now())

        session.add(curSensor)
        session.commit()
        return ret

    @staticmethod
    def check2(inData):
        '''
        :param name:
        :param number:
        :param stationId:
        1: success
        2: username repeat
        ret: {
            0: 'error',
            1: success,
            2:'no name in inData',
            3:'name is empty',
            4:'no number in inData',
            5:'number is empty',
            6:'no ip in inData',
            7:'ip is empty',
            8:'no mac in inData',
            9:'mac is empty',
            10:'no stationId in inData',
            11:'stationId is illegal',
            12:'name repeat',
            13:'number repeat',
            14:'mac repeat',
        }
        '''
        ret = 1
        if('name' not in inData):
            ret = 2
            return ret
        else:
            if(inData['name'] == ''):
                ret = 3
                return ret
        if('number' not in inData):
            ret = 4
            return ret
        else:
            if(inData['number'] == ''):
                ret = 5
                return ret
        if('ip' not in inData):
            ret = 6
            return 6
        else:
            if(inData['ip'] == ''):
                ret = 7
                return ret
        if('mac' not in inData):
            ret = 8
            return ret
        else:
            if(inData['mac'] == ''):
                ret = 9
                return ret

        if('stationId' not in inData):
            ret = 10
            return ret
        else:
            #print('111111111111', inData['stationId'])
            if(inData['stationId'] == ''):
                ret = 11
                return ret
            if(int(inData['stationId']) != 0):
                tmpAllStation = Station.select(
                    {'id': int(inData['stationId'])})
                if(len(tmpAllStation['data']) == 0):
                    ret = 11
                    return ret

        query = session.query(Sensor)
        tmpSensor = query.filter(
            or_(
                Sensor.name == inData['name'],
                Sensor.number == inData['number'],
                Sensor.mac == inData['mac'])).all()
        for tSensor in tmpSensor:
            if(tSensor.name == inData['name']):
                ret = 12
                return ret
            if(tSensor.number == inData['number']):
                ret = 13
                return ret
            if(tSensor.mac == inData['mac']):
                ret = 14
                return ret

        ret = 1
        return ret

    @staticmethod
    def add2(inData):
        ret = Sensor.check2(inData)
        if(ret != 1):
            return ret

        curSensor = Sensor(
            inData['name'],
            inData['number'],
            inData['ip'],
            inData['mac'],
            inData['stationId'],
            datetime.now())
        session.add(curSensor)
        session.commit()
        return ret

    @staticmethod
    def select(inData):
        ret = {}
        ret['status'] = 1
        ret['data'] = []
        ret['pureData'] = []
        query = session.query(Sensor)
        allSensor = None

        if('id' in inData):
            allSensor = query.filter(
                Sensor.id == inData['id'],
                Sensor.valid == 1).all()
        elif('number' in inData):
            allSensor = query.filter(
                Sensor.number == inData['number'],
                Sensor.valid == 1).all()
        elif('name' in inData):
            allSensor = query.filter(
                Sensor.name == inData['name'],
                Sensor.valid == 1).all()
        elif('mac' in inData):
            allSensor = query.filter(
                Sensor.mac == inData['mac'],
                Sensor.valid == 1).all()
        elif('stationId' in inData):
            allSensor = query.filter(
                Sensor.stationId == inData['stationId'],
                Sensor.valid == 1).all()
        else:
            allSensor = query.filter(Sensor.valid == 1).all()

        for tmpData in allSensor:
            tmp = {}
            tmp['id'] = tmpData.id
            tmp['name'] = tmpData.name
            tmp['number'] = tmpData.number
            tmp['ip'] = tmpData.ip
            tmp['mac'] = tmpData.mac
            tmp['stationId'] = tmpData.stationId
            tmp['time'] = tmpData.time

            ret['data'].append(tmp)
            ret['pureData'].append(tmpData)
        return ret

    @staticmethod
    def info(inData):
        from auth import Auth
        pureData = Sensor.select(inData)

        stationInfo = {}
        authInfo = {}
        userInfo = {}

        stationQuery = session.query(Station)
        authQuery = session.query(Auth)
        userQuery = session.query(User)
        for tmp in pureData['data']:
            t = tmp['stationId']

            tmpAllStation = Station.select({'id': int(t)})
            if(len(tmpAllStation['data']) == 0):
                tmp['stationName'] = 'not find'
            else:
                tmp['stationName'] = tmpAllStation['data'][0]['name']

            tmpAllAuth = Auth.select({'sensorId': int(tmp['id'])})
            if(len(tmpAllAuth['data']) == 0):
                tmp['username'] = 'not find'
                tmp['userId'] = -1
            else:
                tmpAllUser = User.select(
                    {'id': int(tmpAllAuth['data'][0]['userId'])})
                if(len(tmpAllUser['data']) == 0):
                    tmp['username'] = 'not find'
                    tmp['userId'] = -1
                else:
                    tmp['username'] = tmpAllUser['data'][0]['username']
                    tmp['userId'] = tmpAllUser['data'][0]['id']

        return pureData

    @staticmethod
    def specialInfo(inData):
        '''
        :param inData:
        :return:{1:'success', 2:'fail'}
        '''
        outInfo = inData['out']
        ret = {}
        ret['status'] = 1
        ret['data'] = []

        if(outInfo['type'] == 'addAuth'):
            allowUsername = None
            if(outInfo['level'] == 0):
                i = 0
                allInfo = Sensor.info({})['data']
                for tmp in allInfo:
                    if(tmp['userId'] == -1):
                        ret['data'].append(tmp)
            else:
                ret['status'] = 2
        else:
            ret['status'] = 2
        # print ret
        return ret

    @staticmethod
    def updateSensor(inData):
        '''
        :param: inData
        :return: {1:'success', 2:'permission denied', 3:'no sensor', 4:'wrong param', 5:'mac repeat', 6:'station id does not exist'}
        '''
        from auth import Auth
        if(('UserId' in inData) and ('SensorId' in inData) and (('Name' in inData) or ('Mac' in inData) or ('Ip' in inData) or ('Number' in inData) or ('StationId' in inData))):
            updateUser = session.query(Auth).filter(
                Auth.userId == inData['UserId'],
                Auth.sensorId == inData['SensorId'],
                Auth.valid == 1).first()
            if(updateUser is None):
                return 2
            tmpSensor = session.query(Sensor).filter(
                Sensor.id == inData['SensorId'], Sensor.valid == 1).first()
            if(tmpSensor is None):
                return 3
            if('Name' in inData and inData['Name'] != ''):
                session.query(Sensor).filter(Sensor.id == inData['SensorId'], Sensor.valid == 1).update(
                    {'name': inData['Name'], 'time': datetime.now()})
            if('Mac' in inData and inData['Mac'] != ''):
                tmpSensorMac = session.query(Sensor).filter(
                    Sensor.valid == 1, Sensor.mac == inData['Mac']).first()
                if(tmpSensorMac is not None):
                    return 5
                session.query(Sensor).filter(Sensor.id == inData['SensorId'], Sensor.valid == 1).update(
                    {'mac': inData['Mac'], 'time': datetime.now()})
            if('Ip' in inData and inData['Ip'] != ''):
                session.query(Sensor).filter(Sensor.id == inData['SensorId'], Sensor.valid == 1).update(
                    {'ip': inData['Ip'], 'time': datetime.now()})
            if('Number' in inData and inData['Number'] != ''):
                session.query(Sensor).filter(Sensor.id == inData['SensorId'], Sensor.valid == 1).update(
                    {'number': inData['Number'], 'time': datetime.now()})
            if('StationId' in inData and inData['StationId'] != ''):
                tmpStation = session.query(Station).filter(
                    Station.id == inData['StationId'], Station.valid == 1).first()
                if(tmpStation is None):
                    return 6
                session.query(Sensor).filter(Sensor.id == inData['SensorId'], Sensor.valid == 1).update(
                    {'stationId': inData['StationId'], 'time': datetime.now()})
            session.commit()
            return 1
        else:
            return 4

    @staticmethod
    def delSensor(inData):
        '''
        :param: inData
        :return: {1:'success', 2:'permission denied', 3:'no sensor', 4:'wrong param', 5:''}
        '''
        from auth import Auth
        from eqp import Eqp
        if(('UserId' in inData) and ('SensorId' in inData)):
            updateUser = session.query(Auth).filter(
                Auth.userId == inData['UserId'],
                Auth.sensorId == inData['SensorId'],
                Auth.valid == 1).first()
            if(updateUser is None):
                updateUserLevel = session.query(
                    User.level).filter(
                    User.id == inData['UserId'],
                    User.valid == 1).first()
                if(updateUserLevel is None or int(updateUserLevel[0]) != 0):
                    return 2
            tmpSensor = session.query(Sensor).filter(
                Sensor.id == inData['SensorId'], Sensor.valid == 1).first()
            if(tmpSensor is None):
                return 3
            session.query(Sensor).filter(Sensor.id == inData['SensorId'], Sensor.valid == 1).update(
                {'valid': 0, 'time': datetime.now()})
            Auth.delAuth({'SensorId': inData['SensorId']})
            Eqp.delEqp({'SensorId': inData['SensorId']})
            session.commit()
            return 1
        else:
            return 4

    @staticmethod
    def update_sensor2(inData):
        '''
        :param inData:
        :return: {0:'errror', 1:'success', 2:'no this id', 3:'iData has no key id', 21:''}
        '''
        ret = 1
        if('id' not in inData):
            ret = 3
            return ret
        query = session.query(Sensor)
        tmpSensor = query.filter(Sensor.id == inData['id']).first()
        if(tmpSensor is None):
            ret = 2
            return ret
        if('name' in inData):
            tmpSensor.name = inData['name']
        if('number' in inData):
            tmpSensor.number = inData['number']
        if('ip' in inData):
            tmpSensor.ip = inData['ip']
        if('mac' in inData):
            tmpSensor.mac = inData['mac']
        if('stationId' in inData):
            if(int(inData['stationId']) != 0):
                stationQuery = session.query(Station)
                tmpStation = stationQuery.filter(
                    Station.id == inData['stationId']).first()
                if(tmpStation is None):
                    ret = 21
                    return ret
                else:
                    tmpSensor.stationId = tmpStation.id
            else:
                tmpSensor.stationId = 0
        session.commit()
        return ret


init_db()
