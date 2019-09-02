
from flask import session


def verify_user():
    pass


def is_allowed(session):
    ret = 1
    if(('id' in session) and ('username' in session) and ('level' in session)):
        verifyRst = User.verifyUser(
            {'id': session['id'], 'username': session['username'], 'level': session['level']})
        if(verifyRst['status'] == 5):
            ret = 1
        else:
            ret = 0
    else:
        ret = 0
    if(ret == 0):
        if('id' in session):
            del session['id']
        if('username' in session):
            del session['username']
        if('level' in session):
            del session['level']
    return ret
