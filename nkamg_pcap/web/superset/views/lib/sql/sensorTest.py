from sensor import Sensor

#ret=Sensor.check('sensor-name-test', 'sensor-number-test', 'sesnor-ip-test', 'sensor-mac-test', 1)
#ret = Sensor.check('')
#ret = Sensor.updateSensor({'UserId':2,'SensorId':2, 'Mac':'qe:rq:tq'})
ret = Sensor.delSensor({'UserId': 2, 'SensorId': 2})

print(ret)

# tmp=Sensor.info({})


# print('111')
# print(tmp)
