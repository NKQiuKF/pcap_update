from connect import engine, session, BaseModel, init_db, drop_db
from sqlalchemy import Column, or_, desc
from sqlalchemy.types import String, Integer, String, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime


class Host(BaseModel):
    __tablename__ = 'host'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    count = Column(Integer, default=0)
    ftime = Column(DateTime)
    ltime = Column(DateTime)

    def __init__(self, name, count, ftime, ltime):
        self.name = name
        self.count = count
        if(ftime is not None):
            self.ftime = ftime
        else:
            self.ftime = datetime.now()
        if(ltime is not None):
            self.ltime = ltime
        else:
            self.ltime = datetime.now()

    def __repr__(self):
        return '<host: %r %r>' % (self.id, self.name)

    @staticmethod
    def info(num):
        ret = {}
        ret['data'] = []
        query = session.query(Host)
        pureData = query.filter().order_by(desc(Host.count)).limit(num).all()
        for tmpData in pureData:
            tmp = {}
            tmp['name'] = tmpData.name
            tmp['count'] = tmpData.count
            ret['data'].append(tmp)
        return ret

    @staticmethod
    def check(name):
        '''
        :param name:
        :return: {1:'success', 2:'name repeat', 3:'name is empty'}
        '''
        if(name == ''):
            return 3
        query = session.query(Host)
        tmpHost = query.filter(Host.name == name).first()
        if(tmpHost is not None):
            return 2
        return 1

    @staticmethod
    def add(name, count=0):
        '''
        :param name:
        :return: {1:'success', 2:'name repeat'}
        '''
        ret = 1
        ret = Host.check(name)
        if(ret != 1):
            return ret
        if(count == 0):
            count = 1
        ftime = datetime.now()
        ltime = datetime.now()
        curHost = Host(name, count, ftime, ltime)

        Session = scoped_session(sessionmaker(autoflush=True, bind=engine))
        Session.add(curHost)
        Session.commit()
        Session.close()
        # session.add(curHost)
        # session.commit()
        return ret

    @staticmethod
    def updateHost(Name_DICT={}):
        '''
        :param Name_DICT:
        :return: {1:'success', 2:'name is empty', 3:'failed'}
        '''
        try:
            if(Name_DICT is None):
                return 3
            for name in Name_DICT.keys():
                #print("add name: %s" %name)
                ret = 1
                ret = Host.check(name)
                if(ret == 1):
                    Host.add(name, Name_DICT[name])
                    continue
                elif(ret == 2):
                    curCount = session.query(
                        Host.count).filter(
                        Host.name == name).first()
                    if(curCount is None):
                        continue
                    else:
                        count = int(curCount[0]) + Name_DICT[name]
                        session.query(Host).filter(Host.name == name).update(
                            {'count': count, 'ltime': datetime.now()})
                        session.commit()
                else:
                    continue
        except BaseException:
            session.rollback()
        finally:
            session.close()
        return 1


init_db()
