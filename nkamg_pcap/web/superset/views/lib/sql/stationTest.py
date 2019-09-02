#!/usr/bin/env python

from station import Station

#ret = Station.updateStation({'UserId':1,'StationId':1, 'Number':'001', 'phone':110})
ret = Station.delStation({'UserId': 1, 'StationId': 1})
print(ret)
