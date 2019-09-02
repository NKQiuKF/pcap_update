from lib.sql.user import User


def is_session_valid(session):
    '''
    Return Value:
        True: session is valied
        False: session is not valid
    '''
    # Check integrity
    if (not session) or ('user_id' not in session) or \
            ('user_name' not in session) or ('user_level' not in session):
        # remove user info from the session if it's there
        session.pop('user_name', None)
        session.pop('user_id', None)
        session.pop('user_level', None)
        return False
    # Check user existence
    if User.is_exist_with_level(user_name=session['user_name'],
                                user_id=session['user_id'],
                                user_level=session['user_level']):
        return True
    return False
