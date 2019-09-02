def hasEqp(InEqp, mac):
    curEqp = InEqp.query.filter_by(mac=mac).first()
    if curEqp is None:
        return 0
    else:
        return 1


def addEqp(db, InEqp, name, ip, mac, sensorId):
    if hasEqp(InEqp, mac) == 1:
        return -1
    curEqp = InEqp(name, ip, mac, sensorId)
    db.session.add(curEqp)
    db.session.commit()


def getAllEqp(InEqp):
    ret = InEqp.query.all()
    return ret
