from connect import engine, session, BaseModel, init_db, drop_db
from sqlalchemy import Column, or_, desc
from sqlalchemy.types import String, Integer, String, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime


class Host2(BaseModel):
    __tablename__ = 'host2'
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
        return '<host2: %r %r>' % (self.id, self.name)

    @staticmethod
    def info(num):
        ret = {}
        ret['data'] = []
        query = session.query(Host2)
        pureData = query.filter().order_by(desc(Host2.count)).limit(num).all()
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
        query = session.query(Host2)
        tmpHost2 = query.filter(Host2.name == name).first()
        if(tmpHost2 is not None):
            return 2
        return 1

    @staticmethod
    def add(name, count=0):
        '''
        :param name:
        :return: {1:'success', 2:'name repeat'}
        '''
        ret = 1
        ret = Host2.check(name)
        if(ret != 1):
            return ret
        if(count == 0):
            count = 1
        ftime = datetime.now()
        ltime = datetime.now()
        curHost2 = Host2(name, count, ftime, ltime)

        Session = scoped_session(sessionmaker(autoflush=True, bind=engine))
        Session.add(curHost2)
        Session.commit()
        Session.close()
        return ret

    @staticmethod
    def updateHost2(Name_DICT={}):
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
                ret = Host2.check(name)
                if(ret == 1):
                    Host2.add(name, Name_DICT[name])
                    continue
                elif(ret == 2):
                    curCount = session.query(
                        Host2.count).filter(
                        Host2.name == name).first()
                    if(curCount is None):
                        continue
                    else:
                        count = int(curCount[0]) + Name_DICT[name]
                        session.query(Host2).filter(Host2.name == name).update(
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
