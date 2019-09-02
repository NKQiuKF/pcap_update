from connect import engine, session, BaseModel, init_db, drop_db
from sqlalchemy import Column, ForeignKey, or_, func, and_
from sqlalchemy.types import String, Integer, DateTime, Float, BigInteger, DECIMAL
import time
from sensor import Sensor


class Atkinfo(BaseModel):
    __tablename__ = 'atkinfo2'
    id = Column(BigInteger, primary_key=True)
    atkId = Column(Integer)
    atkTime = Column(BigInteger, index=True)
    sensorMac = Column(String(80))
    atkType = Column(String(100))

    srcIp = Column(String(20))
    srcPort = Column(String(10))
    srcLng = Column(DECIMAL(16, 10))
    srcLat = Column(DECIMAL(16, 10))

    dstIp = Column(String(20))
    dstPort = Column(String(10))
    dstLng = Column(DECIMAL(16, 10))
    dstLat = Column(DECIMAL(16, 10))

    cmProtocal = Column(String(40))
    trails = Column(String(600))
    refer = Column(String(600))
    infos = Column(String(100))

    def __init__(
            self,
            atkId,
            atkTime,
            sensorMac,
            atkType,
            srcIp,
            srcPort,
            srcLng,
            srcLat,
            dstIp,
            dstPort,
            dstLng,
            dstLat,
            cmProtocal,
            trails,
            refer,
            infos):

        self.atkId = atkId
        self.atkTime = atkTime
        self.sensorMac = sensorMac
        self.atkType = atkType

        self.srcIp = srcIp
        self.srcPort = srcPort
        self.srcLng = srcLng
        self.srcLat = srcLat

        self.dstIp = dstIp
        self.dstPort = dstPort
        self.dstLng = dstLng
        self.dstLat = dstLat

        self.cmProtocal = cmProtocal
        self.trails = trails
        self.refer = refer
        self.infos = infos

    def __repr__(self):
        return '<%s>' % (self.atkTime)

    @staticmethod
    def retData(timeSpan, inType):
        if(inType == 'py'):
            query = session.query(Atkinfo)
            sensorQuery = session.query(Sensor)
            nowTime = time.time()
            limitTime = nowTime - timeSpan
            allInfos = query.filter(
                and_(
                    Atkinfo.pyRead == 0,
                    Atkinfo.atkTime > limitTime))
            ret = []
            for tmpInfo in allInfos:
                tmpInfo.pyRead = 1
                tmp = {}
                tmp['attackId'] = tmpInfo.atkId
                tmp['time'] = time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.localtime(
                        tmpInfo.atkTime))

                tmpSensor = sensorQuery.filter(
                    Sensor.mac == tmpInfo.sensorMac).first()
                if(tmpSensor is not None):
                    tmp['sensorId'] = tmpSensor.number
                else:
                    tmp['sensorId'] = 'not known'

                tmp['src'] = {}
                tmp['src']['ip'] = tmpInfo.srcIp
                tmp['src']['port'] = tmpInfo.srcPort
                tmp['src']['lng'] = float(tmpInfo.srcLng)
                tmp['src']['lat'] = float(tmpInfo.srcLat)
                tmp['src']['name'] = ''

                tmp['dst'] = {}
                tmp['dst']['ip'] = tmpInfo.dstIp
                tmp['dst']['port'] = tmpInfo.dstPort
                tmp['dst']['lng'] = float(tmpInfo.dstLng)
                tmp['dst']['lat'] = float(tmpInfo.dstLat)
                tmp['dst']['name'] = ''

                tmp['protocalA'] = tmpInfo.cmProtocal
                tmp['trails'] = tmpInfo.trails
                tmp['references'] = tmpInfo.refer
                tmp['infos'] = tmpInfo.infos
                ret.append(tmp)
                session.delete(tmpInfo)

            session.commit()
            return ret
        else:
            return {}

    @staticmethod
    def add(
            atkId,
            atkTime,
            sensorMac,
            atkType,
            srcIp,
            srcPort,
            srcLng,
            srcLat,
            dstIp,
            dstPort,
            dstLng,
            dstLat,
            cmProtocal,
            trails,
            refer,
            infos):
        curAtkinfo = Atkinfo(
            atkId,
            atkTime,
            sensorMac,
            atkType,
            srcIp,
            srcPort,
            srcLng,
            srcLat,
            dstIp,
            dstPort,
            dstLng,
            dstLat,
            cmProtocal,
            trails,
            refer,
            infos)
        session.add(curAtkinfo)
        session.commit()


init_db()
