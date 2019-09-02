# coding=utf-8
import os
import multiprocessing
import re
import csv
import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

#from lib.sql.atkinfo import Atkinfo
#------------------------------#
#from lib.settings import config
#from lib.settings import CONFIG_FILE
#from lib.settings import read_config
#------------------------------#


async_mode = None


timeItv2 = 10    # read web_log cycle time
timeItv2a = 2    # if no data, sleep timeItv2a then continue read db

sendTimes = 10  # when read data from db, not send data at once, but send it by sendTimes times

timeItv3 = 100000  # web_log record delay time or time window

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass
    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass
    if async_mode is None:
        async_mode = 'threading'

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'what are you nong sha lai!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
lastTime = 0


def readFile(file_name, curLine):

    if not os.path.exists(file_name):
        print('NO~~~~~~~~~~~~~~~~~~~~~')

    print("Reading atkinfo.csv ...")
    f = open(file_name, 'r')
    reader = csv.reader(f)
    retArray = []
    i = 0
    global lastTime
    for each_line in reader:
        if len(each_line) != 16:
            break
        timeA = each_line[1]
        if i < curLine:
            i += 1
            continue
        attackId = each_line[0]
        sensorId = each_line[2]

        srcIP = each_line[4]
        srcPort = each_line[5]

        dstIP = each_line[8]
        dstPort = each_line[9]

        protocal = each_line[12]

        trails = each_line[13]
        infos = each_line[15]
        references = each_line[14]

        srcLng = each_line[6]
        srcLat = each_line[7]

        dstLng = each_line[10]
        dstLat = each_line[11]

        retData = {
            'attackId': attackId,
            'time': timeA,
            'src': {
                'lat': srcLat,
                'lng': srcLng,
                'ip': srcIP,
                'port': srcPort,
                'name': ''},
            'dst': {
                'lat': dstLat,
                'lng': dstLng,
                'ip': dstIP,
                'port': dstPort,
                'name': ''},
            'sensorId': sensorId,
            'protocalA': protocal,
            'trails': trails,
            'infos': infos,
            'references': references}
        retArray.append(retData)
        i += 1

    curLine = i
    print("curLine2: ", curLine)
    f.close()
    return retArray, curLine


# def send_thread(sendData):
#     """Example of how to send server generated events to clients."""
#     dataLen = len(sendData)
#     print(dataLen)
#     if len(sendData) == 0:
#         time.sleep(timeItv2a)
#         return
#     everyLen = dataLen / sendTimes
#     if everyLen == 0:
#         everyLen = 1
#     everySleep = timeItv2 / sendTimes
#     for i in range(sendTimes):
#         startI = i * everyLen
#         stopI = (i + 1) * everyLen
#         if stopI == startI:
#             stopI += 1
#         print("startI:", startI, " stopI:", stopI)
#         socketio.emit('attack array', sendData[startI:stopI])
#         time.sleep(everySleep)
#     return

# set conf for wsConfig.js
# path=os.getcwd()
# def _set_wsconfig(ip):
#    fp=file(path+'/static/js/wsConfig.js','r+')
#    lines=fp.readlines()
#    new_lines = []
#    for line in lines:
#        if "HOST_IP" in line:
#            line = re.sub(r"host:'.*//HOST_IP", r"host:'"+ip+r"' //HOST_IP", line)
#            new_lines.append(line)
#        else:
#            new_lines.append(line)
#    fp.close()
#    fp=file(path+'/static/js/wsConfig.js','w+')
#    fp.writelines(new_lines)
#    fp.close()
#-------------------------------------------------------
# set conf for ipviking.js
# def _set_2dconfig(ip):
#    fp=file(path+'/static/2d/js/ipviking.js','r+')
#    lines=fp.readlines()
#    new_lines = []
#    for line in lines:
#        if "HOST_IP" in line:
#            line = re.sub(r"ws://.*//HOST_IP", r'ws://'+ip+r':8080/", //HOST_IP', line)
#            new_lines.append(line)
#        else:
#            new_lines.append(line)
#    fp.close()
#    fp=file(path+'/static/2d/js/ipviking.js','w+')
#    fp.writelines(new_lines)
#    fp.close()
#-------------------------------------------------------


# def background_thread():
#     while True:
#         sendData = readDb(timeItv3)
#         thread = Thread(target=send_thread, args=(sendData,))
#         thread.daemon = True
#         thread.start()
#         time.sleep(1)
#
#

your_path = os.path.abspath('..')
print(your_path)
atkinfo_csv_file = '{your_path}/web/superset/views/web_atkinfo.csv'.format(your_path=your_path)


def background_thread():
    curLine = 0
    sendTimes = 10
    # print('1234')
    while True:
        sendData, curLine = readFile(atkinfo_csv_file, curLine)
        print("curLine: ", curLine)
        dataLen = len(sendData)
        if(len(sendData) == 0):
            time.sleep(timeItv2)
            break
        everyLen = dataLen / sendTimes
        if(everyLen == 0):
            everyLen = 1
        everySleep = timeItv2 / sendTimes
        for i in range(sendTimes):
            startI = i * everyLen
            stopI = (i + 1) * everyLen
            if(stopI == startI):
                stopI = stopI + 1
            print("startI:", startI, " stopI:", stopI)
            socketio.emit('attack array', sendData[startI:stopI])
            time.sleep(everySleep)
def back_test():
    while True:
        background_thread()

@socketio.on('connect')
def deal_ws_connect():
    global thread
    if thread is None:
        thread = Thread(target=back_test)
        thread.daemon = True
        thread.start()

# def run_ws2():
#    read_config(CONFIG_FILE)
#    _set_wsconfig(str(config.HOST_IP))
#    _set_2dconfig(str(config.HOST_IP))
#
#    #socketio.run(app, port=1234, host='192.168.0.40', debug=True )
#    socketio.run(app, port=1234, host=str(config.HOST_IP))

# def run_ws2():
#    p = multiprocessing.Process(target = main)
#    p.daemon = True
#    p.start()


if __name__ == '__main__':
    socketio.run(app, port=1234, host='202.112.50.150')
