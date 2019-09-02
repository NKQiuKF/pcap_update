from connect import engine, session, BaseModel, init_db, drop_db
from sqlalchemy import Column, or_
from sqlalchemy.types import String, Integer, String, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

class Outip2(BaseModel):
    __tablename__ = 'outip2'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    count = Column(Integer, default=0)
    ftime = Column(DateTime)
    ltime = Column(DateTime)

    def __init__(self,name,count,ftime,ltime):
        self.name = name
        self.count = count
        if(ftime != None):
            self.ftime = ftime
        else:
            self.ftime = datetime.now()
        if(ltime != None):
            self.ltime = ltime
        else:
            self.ltime = datetime.now()

    def __repr__(self):
        return '<outip2: %r %r>' % (self.id, self.name)

    @staticmethod
    def check(name):
        '''
        :param name:
        :return: {1:'success', 2:'name repeat', 3:'name is empty'}
        '''
        if(name == ''):
            return 3
        Session = scoped_session(sessionmaker(autoflush=True, bind=engine))
        query = Session.query(Outip2)
        tmpAgent = query.filter(Outip2.name == name).first()
        Session.close()
        if(tmpAgent != None):
            return 2
        return 1

    @staticmethod
    def add(name,count=0):
        '''
        :param name:
        :return: {1:'success', 2:'name repeat'}
        '''
        ret = 1
        ret = Outip2.check(name)
        if(ret != 1):
            return ret
        if(count == 0):
            count = 1
        ftime = datetime.now()
        ltime = datetime.now()
        curAgent = Outip2(name,count,ftime,ltime)

        Session = scoped_session(sessionmaker(autoflush=True, bind=engine))
        Session.add(curAgent)
        Session.commit()
        Session.close()
        #session.add(curAgent)
        #session.commit()
        return ret

    @staticmethod
    def updateAgent(Name_DICT = {}):
        '''
        :param Name_DICT:
        :return: {1:'success', 2:'name is empty', 3:'failed'}
        '''
        try:
            Session = scoped_session(sessionmaker(autoflush=True, bind=engine))
            if(Name_DICT == None):
                return 3
            for name in Name_DICT.keys():
                #print("add name: %s" %name)
                ret = 1
                ret = Outip2.check(name)
                if(ret == 1):
                    Outip2.add(name,Name_DICT[name])
                    continue
                elif(ret == 2):
                    curCount = Session.query(Outip2.count).filter(Outip2.name == name).first()
                    if(curCount == None):
                        continue
                    else:
                        count = int(curCount[0]) + Name_DICT[name]
                        Session.query(Outip2).filter(Outip2.name == name).update({'count':count, 'ltime':datetime.now()})
                        Session.commit()
                else:
                    continue
        except:
            Session.rollback()
            #raise
        finally:
            Session.close()
        return 1;

init_db()
