import re
from time import sleep
lastData={}

def readNet():
    f=open('/proc/net/dev', 'r')
    allData=f.readlines()
    reg=re.compile('\s*([a-z0-9]+):\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+')
    ret={}
    for i in range(2, (len(allData))):
	matchData=reg.match(allData[i])
        ethName=matchData.group(1)
        ethRecv=int(matchData.group(2))
        ethSend=int(matchData.group(10))
        tmp={}
        tmp['name']=ethName
        tmp['recv']=ethRecv
        tmp['send']=ethSend
        ret[ethName]=tmp.copy()
        if(ethName in lastData):
            ret[ethName]['recv']=ret[ethName]['recv']-lastData[ethName]['recv']
            ret[ethName]['send']=ret[ethName]['send']-lastData[ethName]['send']
        else:
            ret[ethName]['recv']=0
            ret[ethName]['send']=0

        lastData[ethName]=tmp.copy()

        return ret
    f.close()

def test():
    while(True):
        sleep(1)
        tmp=readNet()
        print(tmp)

if __name__=='__main__':
    test()