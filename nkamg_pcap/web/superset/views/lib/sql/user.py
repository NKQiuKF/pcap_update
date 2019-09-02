from connect import engine, session, BaseModel, init_db, drop_db
from sqlalchemy import Column
from sqlalchemy.types import String, Integer, DateTime
from datetime import datetime
import hashlib


class User(BaseModel):
    __tablename__ = 'userv2'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    passwd = Column(String(100), nullable=False)
    level = Column(Integer)
    time = Column(DateTime)
    valid = Column(Integer, default=1)

    def __init__(self, username, passwd, level):
        self.username = username
        pwMD5 = hashlib.md5()
        pwMD5.update("%s%s" % (username, passwd))
        self.passwd = str(pwMD5.hexdigest())
        self.level = level
        self.time = datetime.now()

    def __repr__(self):
        return '<id: %r %r %d %r>' % (
            self.id, self.username, self.level, self.passwd)

    @staticmethod
    def check(username):
        ret = 1
        query = session.query(User)
        tmpUser = query.filter_by(username=username, valid=1).first()
        # tmpUser=query.filter(User.username==username).first()
        if(tmpUser is not None):
            ret = 3
        return ret

    @staticmethod
    def add(username, passwd, level):
        '''
        1: success
        2: out:two passwd are not same
        3: username repeat
        '''
        ret = 1
        tmp = User.check(username)
        if(tmp == 1):
            curUser = User(username, passwd, level)
            session.add(curUser)
            session.commit()
        else:
            ret = tmp
        return ret

    @staticmethod
    def select(inData):
        ret = {}
        ret['data'] = []
        ret['pureData'] = []
        ret['status'] = 1
        query = session.query(User)
        allUser = None
        if('id' in inData):
            allUser = query.filter(
                User.id == inData['id'],
                User.valid == 1).all()
        elif('username' in inData):
            allUser = query.filter(
                User.username == inData['username'],
                User.valid == 1).all()
        elif('level' in inData):
            allUser = query.filter(
                User.level == inData['level'],
                User.valid == 1).all()
        else:
            allUser = query.filter(User.valid == 1).all()
        # print allUser
        for tmpData in allUser:
            tmp = {}
            tmp['id'] = tmpData.id
            tmp['username'] = tmpData.username
            tmp['level'] = tmpData.level
            # tmp['passwd']=tmpData.passwd
            ret['data'].append(tmp)
            ret['pureData'].append(tmpData)

        return ret

    @staticmethod
    def getMd5Pw(username, passwd):
        pwMd5 = hashlib.md5()
        pwMd5.update("%s%s" % (username, passwd))
        curPw = str(pwMd5.hexdigest())
        return curPw

    @staticmethod
    def changePw(inData):
        '''
        :param inData:
        :return: {1:'success', '4':'fail', '3':'username repeat'}
        '''
        #print('cccccccccccccc', inData)
        if(('id' in inData) and ('newUsername' in inData) and ('newPasswd' in inData)):
            userData = User.select(inData)
            if(len(userData['pureData']) == 1):
                curUser = userData['pureData'][0]
                if(inData['newUsername'] == curUser.username):
                    curUser.passwd = User.getMd5Pw(
                        inData['newUsername'], inData['newPasswd'])
                    session.commit()
                    return 1
                else:
                    antUserData = User.select(
                        {'username': inData['newUsername']})
                    if(len(antUserData['pureData']) != 0):
                        return 3
                    else:
                        curUser.username = inData['newUsername']
                        curUser.passwd = User.getMd5Pw(
                            inData['newUsername'], inData['newPasswd'])
                        session.commit()
                        return 1
            else:
                return 4
        else:
            return 4

    @staticmethod
    def verifyUser(inData):
        '''
        :param inData:
        :return: {1:'(username passwd)success', 2:'no user', 3:'passwd wrong', 4:'input nouser or nopasswd', 5:'(id, username, level)success', 6:'id right, but username or level wrong', 7:'wrong'}
        '''
        ret = {}
        ret['status'] = 1
        if(('username' in inData) and ('passwd' in inData)):
            # print 1
            inputMd5 = User.getMd5Pw(inData['username'], inData['passwd'])
            #print('user'+str(inData['username'])+' pass:'+str(inData['passwd']))
            # print inputMd5
            userData = User.select({'username': inData['username']})
            # print str(userData['pureData'])
            if(len(userData['pureData']) == 0):
                ret['status'] = 2
                # print 2
            else:
                # print userData['pureData']
                # print 3
                rightUser = userData['pureData'][0]
                rightMd5 = rightUser.passwd
                # print(rightUser)
                if(inputMd5 == rightMd5):
                    # print 4
                    ret['status'] = 1
                    ret['id'] = rightUser.id
                    ret['username'] = rightUser.username
                    ret['level'] = rightUser.level
                else:
                    # print 5
                    ret['status'] = 3
        elif(('username' in inData) and ('level' in inData) and('id' in inData)):
            # print 6
            userData = User.select({'id': inData['id']})

            if(len(userData['pureData']) == 1):
                rightUser = userData['pureData'][0]
                # print 7
                if((rightUser.username == inData['username']) and (rightUser.level == inData['level'])):
                    ret['status'] = 5
                    # print 8
                else:
                    ret['status'] = 6
                    # print 9
            else:
                # print 10
                ret['status'] = 7
        # print ret
        return ret

    @staticmethod
    def updateUser(inData):
        '''
        :param inData:
        :return: {1:'update success', 2:'no user', 3:'permission denied', 4:'username repeat', 5:'failed(wrong param)'}
        '''
        if(('updateId' in inData) and ('id' in inData) and (('newUsername' in inData) or ('newPasswd' in inData) or ('newLevel' in inData))):
            updateUserLevel = session.query(
                User.level).filter(
                User.id == inData['updateId'],
                User.valid == 1).first()
            if(updateUserLevel is None or int(updateUserLevel[0]) != 0):
                return 3
            else:
                chgUser = session.query(User).filter(
                    User.id == inData['id'], User.valid == 1).first()
                if(chgUser is None):
                    return 2
                if('newUsername' in inData and inData['newUsername'] != ''):
                    tmp = User.check(inData['newUsername'])
                    if(tmp == 1):
                        session.query(User).filter(User.id == inData['id']).update(
                            {'username': inData['newUsername'], 'time': datetime.now()})
                    else:
                        return 4
                if('newPasswd' in inData and inData['newPasswd'] != ''):
                    userName = session.query(
                        User.username).filter(
                        User.id == inData['id']).first()
                    md5Passwd = User.getMd5Pw(userName[0], inData['newPasswd'])
                    session.query(User).filter(User.id == inData['id']).update(
                        {'passwd': md5Passwd, 'time': datetime.now()})
                if('newLevel' in inData and inData['newLevel'] != ''):
                    session.query(User).filter(User.id == inData['id']).update(
                        {'level': inData['newLevel'], 'time': datetime.now()})
                session.commit()
                return 1
        else:
            return 5

    @staticmethod
    def deleteUser(inData):
        '''
        :param inData:
        :return: {1:'success', 2:'no user', 3:'permission denied', 4:'failed'}
        '''
        from auth import Auth
        if(('updateId' in inData) and ('delId' in inData)):
            updateUserLevel = session.query(
                User.level).filter(
                User.id == inData['updateId'],
                User.valid == 1).first()
            if(updateUserLevel is None or int(updateUserLevel[0]) != 0):
                return 3
            else:
                chgUser = session.query(User).filter(
                    User.id == inData['delId'], User.valid == 1).first()
                if(chgUser is None):
                    return 2
                else:
                    session.query(User).filter(User.id == inData['delId']).update(
                        {'valid': 0, 'time': datetime.now()})
                    session.commit()
                    Auth.delAuth({'UserId': inData['delId']})
                    return 1
        else:
            return 4

    @staticmethod
    def del_user2(inData):
        '''
        :param inData:
        :return{0: error, 2: no id in inData, 3: no such id in userv2, }:
        '''
        ret = 0
        if('id' not in inData):
            ret = 2
            return ret
        query = session.query(User)
        tmpUser = query.filter(User.id == inData['id']).first()
        if(tmpUser is None):
            ret = 3
            return ret
        else:
            from user_old import User_old
            User_old.add(tmpUser)
            from auth import Auth
            authQuery = session.query(Auth)
            authQuery.filter(Auth.userId == tmpUser.id).delete()
            session.delete(tmpUser)
            session.commit()
            ret = 1
            return ret

    @staticmethod
    def update_user2(inData):
        '''
        :param inData:
        :return: {
            1:'success',
            12:'no id',
            13:'id not exist',
            14:'username is none',
            15:'level is illegal',
            16:'passwd is too short',
            17:'already has user'
        }
        '''
        ret = 1
        if('id' not in inData):
            ret = 12
            return ret
        query = session.query(User)
        tmpUser = query.filter(User.id == inData['id']).first()
        if(tmpUser is None):
            ret = 13
            return ret
        if('username' in inData):
            tmpUser2 = query.filter(
                User.username == inData['username']).first()
            if(tmpUser2 is not None):
                ret = 17
                return ret
            if(inData['username'] != ''):
                tmpUser.username = inData['username']
            else:
                ret = 14
                return ret
        if('level' in inData):
            inData['level'] = int(inData['level'])
            if((inData['level'] == 0) or (inData['level'] == 1) or (inData['level'] == 2)):
                tmpUser.level = inData['level']
            else:
                ret = 15
                return ret
        if('passwd' in inData):
            if(len(inData['passwd']) < 6):
                ret = 16
                return ret
            else:
                tmpUser.passwd = User.getMd5Pw(
                    tmpUser.username, inData['passwd'])

        session.commit()
        return ret


init_db()
