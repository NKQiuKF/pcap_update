from user import User
from eqp import Eqp
#

Eqp.add(
    'eqp-name1',
    'eqp-number1',
    'ip1',
    'mac1',
    None,
    None,
    1,
    '11:11:11:11:11:11')
Eqp.add(
    'eqp-name2',
    'eqp-number2',
    'ip2',
    'mac2',
    None,
    None,
    1,
    '11:11:11:11:11:11')
Eqp.add(
    'eqp-name3',
    'eqp-number3',
    'ip3',
    'mac3',
    None,
    None,
    1,
    '11:11:11:11:11:11')
Eqp.add(
    'eqp-name4',
    'eqp-number4',
    'ip4',
    'mac4',
    None,
    None,
    1,
    '11:11:11:11:11:11')


Eqp.add(
    'eqp-name11',
    'eqp-number11',
    'ip11',
    'mac11',
    None,
    None,
    1,
    '22:22:22:22:22:22')
Eqp.add(
    'eqp-name12',
    'eqp-number12',
    'ip12',
    'mac12',
    None,
    None,
    1,
    '22:22:22:22:22:22')
Eqp.add(
    'eqp-name13',
    'eqp-number13',
    'ip13',
    'mac13',
    None,
    None,
    1,
    '22:22:22:22:22:22')
Eqp.add(
    'eqp-name14',
    'eqp-number14',
    'ip14',
    'mac14',
    None,
    None,
    1,
    '22:22:22:22:22:22')

ret = User.add('a', '1', 0)
print(ret)
#
# tmp=User.changePw({'id':1, 'newPasswd':'1234', 'newUsername':'asd'})
# print(tmp)
# #
# print(User.verifyUser({'username':'asd', 'passwd':'123'}))

#tmp=User.add('test', '123', 0)
#tmp = User.deleteUser({'updateId':'1', 'delId':'2'})
#tmp = User.check('test')
# print(tmp)

#print(User.verifyUser({'username':'asd', 'passwd':'123'}))
