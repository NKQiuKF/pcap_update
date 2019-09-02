from connect import engine, session, BaseModel, init_db, drop_db
from sqlalchemy import Column, or_, desc
from sqlalchemy.types import String, Integer, String, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime


class Atktype4(BaseModel):
    __tablename__ = 'atktype4'
    id = Column(Integer, primary_key=True)
    date = Column(String(10), unique=True, nullable=False)
    count = Column(Integer, default=0)
    ftime = Column(DateTime)
    ltime = Column(DateTime)

    def __init__(self, date, count, ftime, ltime):
        self.count = count
        self.date = date
        if(ftime is not None):
            self.ftime = ftime
        else:
            self.ftime = datetime.now()
        if(ltime is not None):
            self.ltime = ltime
        else:
            self.ltime = datetime.now()

    def __repr__(self):
        return '<atktype4: %r %r>' % (self.id, self.date)

    @staticmethod
    def info(num):
        ret = {}
        ret['data'] = []
        query = session.query(Atktype4)
        n = session.query(Atktype4).filter().count()
        pureData = query.offset(n - 7).limit(num).all()
        for tmpData in pureData:
            tmp = {}
            tmp['date'] = tmpData.date
            tmp['count'] = tmpData.count
            ret['data'].append(tmp)
        return ret

    @staticmethod
    def check(date):
        '''
        :param name:
        :return: {1:'success', 2:'name repeat', 3:'name is empty'}
        '''
        if(date == ''):
            return 3
        Session = scoped_session(sessionmaker(autoflush=True, bind=engine))
        query = Session.query(Atktype4)
        tmp = query.filter(Atktype4.date == date).first()
        Session.close()
        if(tmp is not None):
            return 2
        return 1

    @staticmethod
    def add(date, count=0):
        '''
        :param name:
        :return: {1:'success', 2:'name repeat'}
        '''
        ret = 1
        ret = Atktype4.check(date)
        if(ret != 1):
            return ret
        if(count == 0):
            count = 1
        ftime = datetime.now()
        ltime = datetime.now()
        cur = Atktype4(date, count, ftime, ltime)

        Session = scoped_session(sessionmaker(autoflush=True, bind=engine))
        Session.add(cur)
        Session.commit()
        Session.close()

        return ret

    @staticmethod
    def updateatktype4(Date_DICT={}):
        '''
        :param Date_DICT:
        :return: {1:'success', 2:'name is empty', 3:'failed'}
        '''
        try:
            Session = scoped_session(sessionmaker(autoflush=True, bind=engine))
            if(Date_DICT is None):
                return 3
            for date in Date_DICT.keys():
                #print("add name: %s" %name)
                ret = 1
                ret = Atktype4.check(date)
                if(ret == 1):
                    Atktype4.add(date, Date_DICT[date])
                    continue
                elif(ret == 2):
                    curCount = Session.query(
                        Atktype4.count).filter(
                        Atktype4.date == date).first()
                    if(curCount is None):
                        continue
                    else:
                        count = int(curCount[0]) + Date_DICT[date]
                        Session.query(Atktype4).filter(Atktype4.date == date).update(
                            {'count': count, 'ltime': datetime.now()})
                        Session.commit()
                else:
                    continue
        except BaseException:
            Session.rollback()
            # raise
        finally:
            Session.close()
        return 1


init_db()
