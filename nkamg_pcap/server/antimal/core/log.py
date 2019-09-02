#!/usr/bin/env python

"""
Copyright (c) 2014-2016 Miroslav Stampar (@stamparm)
See the file 'LICENSE' for copying permission
"""
#import geoip2
import geoip2.database
#end
import os
import signal
import socket
import SocketServer
import sys
import threading
import traceback
import json
import re
#--------------add by qkf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from atkinfo import Atkinfo
from atkinfo2 import Atkinfo2
import datetime
import time
import random
#--------------end
from core.common import check_sudo
from core.settings import config
from core.settings import CONDENSE_ON_INFO_KEYWORDS
from core.settings import CONDENSED_EVENTS_FLUSH_PERIOD
from core.settings import DEFAULT_ERROR_LOG_PERMISSIONS
from core.settings import DEFAULT_EVENT_LOG_PERMISSIONS
from core.settings import TIME_FORMAT
from core.settings import WHITELIST
#import for DATABASES
from outip import Outip
from outip2 import Outip2
from host import Host
from host2 import Host2
from agent import Agent
from agent2 import Agent2
from domain import Domain
from domain2 import Domain2
from atktype1 import Atktype1
from atktype2 import Atktype2
from atktype3 import Atktype3
from atktype4 import Atktype4
from atktype5 import Atktype5
from atktype6 import Atktype6
Packet_buffer = []
#Last_send_time = datetime(2016,01,01)

_thread_data = threading.local()
#IP_MAC_DICT_SS = {}
#IP_MAC_IN_LOG = []
'''
def GetNowTime():
    return time.strftime("%Y%m%d",time.localtime(time.time()))
'''
axis_num1 = {}
axis_num2 = {}
axis_num3 = {}
axis_num4 = {}
axis_num5 = {}
axis_num6 = {}


OUTIP={}
OUTIP2={}
HOST_DICT = {}
DOMAIN_DICT = {}
BROWSER_DICT = {}
HOST_DICT2 = {}
DOMAIN_DICT2 = {}
BROWSER_DICT2 = {}
FLITER = 0
#geoip2 database reader
reader = geoip2.database.Reader(os.getcwd()+"/geoip/GeoLite2-City.mmdb")




def create_log_directory():
    if not os.path.isdir(config.LOG_DIR):
        if check_sudo() is False:
            exit("[!] please run with sudo/Administrator privileges")
        os.makedirs(config.LOG_DIR)
    print("[i] using '%s' for log storage" % config.LOG_DIR)

def get_event_log_handle(sec, flags=os.O_APPEND | os.O_CREAT | os.O_WRONLY):
    localtime = time.localtime(sec)
    _ = os.path.join(config.LOG_DIR, "%d-%02d-%02d.log" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday))
    if _ != getattr(_thread_data, "event_log_path", None):
        if not os.path.exists(_):
            open(_, "w+").close()
            os.chmod(_, DEFAULT_EVENT_LOG_PERMISSIONS)
        _thread_data.event_log_path = _
        _thread_data.event_log_handle = os.open(_thread_data.event_log_path, flags)
    return _thread_data.event_log_handle

def get_error_log_handle(flags=os.O_APPEND | os.O_CREAT | os.O_WRONLY):
    if not hasattr(_thread_data, "error_log_handle"):
        _ = os.path.join(config.LOG_DIR, "error.log")
        if not os.path.exists(_):
            open(_, "w+").close()
            os.chmod(_, DEFAULT_ERROR_LOG_PERMISSIONS)
        _thread_data.error_log_path = _
        _thread_data.error_log_handle = os.open(_thread_data.error_log_path, flags)
    return _thread_data.error_log_handle

def safe_value(value):
    retval = str(value or '-')
    if any(_ in retval for _ in (' ', '"')):
        retval = "\"%s\"" % retval.replace('"', '""')
    return retval


def log_error(msg):
    try:
        handle = get_error_log_handle()
        os.write(handle, "%s %s\n" % (time.strftime(TIME_FORMAT, time.localtime()), msg))
        os.close(handle)
    except (OSError, IOError):
        if config.SHOW_DEBUG:
            traceback.print_exc()
'''
def Deal_with_DB(IP_MAC_DICT = {}, sensorMac=None):
    if not IP_MAC_DICT or sensorMac == None:
        return
    for ip_list in IP_MAC_DICT.keys():
        Has_name = re.search(" ",IP_MAC_DICT[ip_list])
        if Has_name:
            CPUname, MAC = IP_MAC_DICT[ip_list].split(" ")
        else:
            CPUname = "UnknownHost"
            MAC = IP_MAC_DICT[ip_list]
'''
def info_for_axis(infotype,date):
    global axis_num1
    global axis_num2
    global axis_num3
    global axis_num4
    global axis_num5
    global axis_num6


    if date not in axis_num1:
        axis_num1[date]=0
    if date not in axis_num2:
        axis_num2[date]=0
    if date not in axis_num3:
        axis_num3[date]=0
    if date not in axis_num4:
        axis_num4[date]=0
    if date not in axis_num5:
        axis_num5[date]=0
    if date not in axis_num6:
        axis_num6[date]=0


    if len(axis_num1) >= 1:
        tmp_type1 = axis_num1
        axis_num1 = {}
        Atktype1.updateatktype1(tmp_type1)
    if len(axis_num2) >= 1:
        tmp_type2 = axis_num2
        axis_num2 = {}
        Atktype2.updateatktype2(tmp_type2)
    if len(axis_num3) >= 1:
        tmp_type3 = axis_num3
        axis_num3 = {}
        Atktype3.updateatktype3(tmp_type3)
    if len(axis_num4) >= 1:
        tmp_type4 = axis_num4
        axis_num4 = {}
        Atktype4.updateatktype4(tmp_type4)
    if len(axis_num5) >= 1:
        tmp_type5 = axis_num5
        axis_num5 = {}
        Atktype5.updateatktype5(tmp_type5)
    if len(axis_num6) >= 1:
        tmp_type6 = axis_num6
        axis_num6 = {}
        Atktype6.updateatktype6(tmp_type6)
    if infotype==0:
        if date in axis_num1:
            axis_num1[date]=axis_num1[date]+1
        else:
            axis_num1[date]=1
        return
    if infotype==1:
        if date in axis_num2:
            axis_num2[date]=axis_num2[date]+1
        else:
            axis_num2[date]=1
        return
    if infotype==2:
        if date in axis_num3:
            axis_num3[date]=axis_num3[date]+1
        else:
            axis_num3[date]=1
        return
    if infotype==3:
        if date in axis_num4:
            axis_num4[date]=axis_num4[date]+1
        else:
            axis_num4[date]=1
        return
    if infotype==4:
        if date in axis_num5:
            axis_num5[date]=axis_num5[date]+1
        else:
            axis_num5[date]=1
        return
    if infotype==5:
        if date in axis_num6:
            axis_num6[date]=axis_num6[date]+1
        else:
            axis_num6[date]=1
        return

#---------------------------------------------------

def bad_info_pie(HostInfo, DomainInfo, BrowserInfo,outip):
    global HOST_DICT2
    global DOMAIN_DICT2
    global BROWSER_DICT2
    global OUTIP2
    if len(OUTIP2) >= 1:
        #print("updateHost:")
        tmp_b_dict = OUTIP2
        OUTIP2 = {}
        Outip2.updateAgent(tmp_b_dict)
   
    if len(HOST_DICT2) >= 1:
        #print("updateHost:")
        tmp_host_dict = HOST_DICT2
        HOST_DICT2 = {}
        Host2.updateHost(tmp_host_dict)
    if len(DOMAIN_DICT2) >= 1:
        #print("updateDomain:")
        tmp_dict = DOMAIN_DICT2
        DOMAIN_DICT2 = {}
        Domain2.updateDomain(tmp_dict)
    if len(BROWSER_DICT2) >= 1:
        #print("updateAgent:")
        tmp_agent_dict = BROWSER_DICT2
        BROWSER_DICT2 = {}
        Agent2.updateAgent(tmp_agent_dict)
    if HostInfo != "-":
        if HostInfo in HOST_DICT2:
            HOST_DICT2[HostInfo] = HOST_DICT2[HostInfo] + 1
        else:
            HOST_DICT2[HostInfo] = 1
    if DomainInfo != "-":
        if DomainInfo in DOMAIN_DICT2:
            DOMAIN_DICT2[DomainInfo] = DOMAIN_DICT2[DomainInfo] + 1
        else:
            DOMAIN_DICT2[DomainInfo] = 1
    if BrowserInfo != "-":
        if BrowserInfo in BROWSER_DICT2:
            BROWSER_DICT2[BrowserInfo] = BROWSER_DICT2[BrowserInfo] + 1
        else:
            BROWSER_DICT2[BrowserInfo] = 1
    if outip != "-":
        if outip in OUTIP2:
            OUTIP2[outip] = OUTIP2[outip] + 1
        else:
            OUTIP2[outip] = 1

#--------------------------------------------------
'''
def normal_info_pie(HostInfo, DomainInfo, BrowserInfo,outip):
    global HOST_DICT
    global DOMAIN_DICT
    global BROWSER_DICT
    global OUTIP
    if len(OUTIP) >= 1:
        #print("updateHost:")
        tmp_a_dict = OUTIP
        OUTIP = {}
        Outip.updateAgent(tmp_a_dict)
   
    if len(HOST_DICT) >= 1:
        #print("updateHost:")
        tmp_host_dict = HOST_DICT
        HOST_DICT = {}
        Host.updateHost(tmp_host_dict)
    if len(DOMAIN_DICT) >= 1:
        #print("updateDomain:")
        tmp_dict = DOMAIN_DICT
        DOMAIN_DICT = {}
        Domain.updateDomain(tmp_dict)
    if len(BROWSER_DICT) >= 1:
        #print("updateAgent:")
        tmp_agent_dict = BROWSER_DICT
        BROWSER_DICT = {}
        Agent.updateAgent(tmp_agent_dict)
    if HostInfo != "-":
        if HostInfo in HOST_DICT:
            HOST_DICT[HostInfo] = HOST_DICT[HostInfo] + 1
        else:
            HOST_DICT[HostInfo] = 1
    if DomainInfo != "-":
        if DomainInfo in DOMAIN_DICT:
            DOMAIN_DICT[DomainInfo] = DOMAIN_DICT[DomainInfo] + 1
        else:
            DOMAIN_DICT[DomainInfo] = 1
    if BrowserInfo != "-":
        if BrowserInfo in BROWSER_DICT:
            BROWSER_DICT[BrowserInfo] = BROWSER_DICT[BrowserInfo] + 1
        else:
            BROWSER_DICT[BrowserInfo] = 1
    if outip != "-":
        if outip in OUTIP:
            OUTIP[outip] = OUTIP[outip] + 1
        else:
            OUTIP[outip] = 1
'''
#----------------------------------
def IsInner(a):
    tmp=a.split(".");
    if ((tmp[0]=='10')or (tmp[0]=='192' and tmp[1]=='168') or (tmp[0]=='172' and (tmp[1]>='16' and tmp[1]<='31'))):
        return True;
    else:

        return False;
#----------------------------------------
import pandas as pd
def log_event_for_web(log_list = []):
    global FLITER
    hot_num1=[]
    hot_num2=[]
    #classified by info
    if not log_list or len(log_list) != 14:
        return
    #kaggle_path=os.getcwd()+"/hot_map1.csv"
    log_path = os.getcwd() + "/web_atkinfo.csv"
    handle = os.open(log_path, os.O_APPEND | os.O_CREAT | os.O_WRONLY)
    try:
        if "malware" in log_list[9]:
            atkid=0
            atktype="malware"
        elif "reputation" in log_list[9] or "attacker" in log_list[9]:
            atkid=1
            atktype="hacker"
        elif "spammer" in log_list[9]:
            atkid=2
            atktype="spammer"
        elif "crawler" in log_list[9]:
            atkid=3
            atktype="crawler" 
        elif "compromised" in log_list[9] or "scanning" in log_list[9]:
            atkid=4
            atktype="compromised"
        else:
            atkid = 4 #"suspious"
            atktype="suspious"
        #start get location
        src_longitude, src_latitude, dst_longitude, dst_latitude = "?", "?", "?", "?"
        if IsInner(log_list[2]):
            src_longitude, src_latitude = '?','?'
        else :
	    src_location = reader.city(log_list[2])
	    if src_location:
                src_longitude, src_latitude = round(src_location.location.longitude,2),round(src_location.location.latitude,2)
	        #src_longitude=src_longitude[0:9]
 	        #src_latitude=src_latitude[0:9]
        if IsInner(log_list[4]):
	    dst_longitude, dst_latitude = '?','?'
        else : 
            dst_location = reader.city(log_list[4])
	    if dst_location:
                dst_longitude, dst_latitude = round(dst_location.location.longitude,2), round(dst_location.location.latitude,2)
                #dst_longitude=dst_longitude[0:9]
 	        #dst_latitude=dst_latitude[0:9]
         #end get location 

        
        if  src_longitude!='?' and src_latitude!='?' and dst_longitude!='?' and dst_latitude!='?' :
#------------------------------------------------by qkf  for db   trails too long-------------------------
            #log_list[8]=log_list[8][0:50]
#---------------------------------------------------by  qkf---------------------------
            '''curAtkinfo=Atkinfo(atkid, time.time(), log_list[1],atktype, log_list[2], log_list[3], src_longitude, src_latitude, log_list[4], log_list[5],dst_longitude, dst_latitude, log_list[6], log_list[8], log_list[10], log_list[9])
            curAtkinfo2=Atkinfo2(atkid, time.time(), log_list[1],atktype, log_list[2], log_list[3], src_longitude, src_latitude, log_list[4], log_list[5],dst_longitude, dst_latitude, log_list[6], log_list[8], log_list[10], log_list[9])
            session_for_sql.add(curAtkinfo)
            session_for_sql.commit()
            session_for_sql.add(curAtkinfo2)
            session_for_sql.commit()
            session_for_sql.close()'''
            write_list=[str(atkid), str(log_list[0]), str(log_list[1]),str(atktype), str(log_list[2]), str(log_list[3]), str(src_longitude),str(src_latitude), str(log_list[4]), str(log_list[5]),str(dst_longitude), str(dst_latitude), str(log_list[6]),log_list[8], log_list[10], log_list[9]]
            write_list=','.join(write_list)
            os.write(handle, (write_list+'\n'))
#------------------------------------------------
            #init three csv for kaggle_hot_map
            file_name1='/home/nkamg/nkamg-7.24/web/heat_input/heat_map1.csv'
            file_name2='/home/nkamg/nkamg-7.24/web/heat_input/heat_map2.csv'
            file_name3='/home/nkamg/nkamg-7.24/web/heat_input/heat_map3.csv'
            if not os.path.exists(file_name1):
                file_object = open(file_name1, 'w')  
                file_object.write('event_id,src_ip,timestamp,longitude,latitude\n')  
                file_object.close( )
            if not os.path.exists(file_name2):
                file_object = open(file_name2, 'w')
                file_object.write('src_ip,trail,trail_info\n') 
                file_object.close( )
            if not os.path.exists(file_name3):
                file_object = open(file_name3, 'w')
                file_object.write('src_ip,gender,atkid,atktype\n')
                file_object.close( )
            hot_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            hot_pd1=pd.read_csv(file_name1)
            hot_pd2=pd.read_csv(file_name2)
            hot_pd3=pd.read_csv(file_name3)
            hot_pd3.loc[len(hot_pd3)]=[str(log_list[2]),str(log_list[10]),str(atkid),atktype]
            hot_pd2.loc[len(hot_pd2)]=[str(log_list[2]),str(log_list[8]),log_list[9]]
            hot_pd1.loc[len(hot_pd1)]=[len(hot_pd1),str(log_list[2]),hot_time,str(src_longitude),str(src_latitude)]
            #COLUMNS1=['ip','timestamp','longitude','latitude']
            hot_pd2=hot_pd2.drop_duplicates()
            hot_pd3=hot_pd3.drop_duplicates()

            hot_pd2.to_csv(file_name2,index=False)
            hot_pd1.to_csv(file_name1,index=False)
            hot_pd3.to_csv(file_name3,index=False)

#-----------------------------
            tmp_time=time.strftime("%Y%m%d",time.localtime(time.time()))
            #print tmp_time
            info_for_axis(atkid,tmp_time)
#-----------------------------

    except Exception, ex:
        print(ex)
#----------------------------------------
def start_logd(address=None, port=None, join=False, maltrails = {}): 
    class ThreadingUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
        pass

    class UDPHandler(SocketServer.BaseRequestHandler):
        def handle(self):
            try:
                #global IP_MAC_DICT_SS
                #global IP_MAC_IN_LOG
                data, _ = self.request
                sec, event = data.split(" ", 1)
                #if sec == "IP_MAC_PACKET" or sec == "IP_MAC_HOST_PACKET":
                '''
                if sec == "IP_MAC_HOST_PACKET":
                    sensorMac, ex_event = event.split(" ", 1)
                    IP_MAC_DICT = json.loads(ex_event)
                    Deal_with_DB(IP_MAC_DICT, sensorMac)
                    #for key_ip, value_mac in IP_MAC_DICT.items():
                        #if key_ip not in IP_MAC_DICT_SS:
                            #IP_MAC_DICT_SS[key_ip] = value_mac
                #elif sec == "IP_MAC_HOST_PACKET":
                    #Host_LIST = json.loads(event)   
                '''                 
                #else:
                handle = get_event_log_handle(int(sec))
                #search maltrails
                log_list = event.strip("\n").split("** ",-1)
                if len(log_list) != 14:
                    return
                src_ip = log_list[2]
                dst_ip = log_list[4]
                trail = log_list[8]
                log_list[9] = maltrails[trail][0]
                log_list[10] = maltrails[trail][1]
                '''
                if trail and trail in maltrails:
                    tmpo=0
                    log_list[9] = maltrails[trail][0]
                    log_list[10] = maltrails[trail][1]
                elif src_ip in maltrails:
                    tmpo=1
                    log_list[8] = src_ip
                    log_list[9] = maltrails[src_ip][0]
                    log_list[10] = maltrails[src_ip][1]
                elif dst_ip in maltrails:
                    tmpo=2
                    log_list[8] = dst_ip
                    log_list[9] = maltrails[dst_ip][0]
                    log_list[10] = maltrails[dst_ip][1]
                else:
                    log_list[9] = "benign"
                    

                if log_list[9] == "benign":
                    Add_Host_inDB(log_list[11], log_list[12],log_list[2],log_list[4])
                    
                else:
               
                    if tmpo==0:
                        Add_Host_inDB2(log_list[11], log_list[12],log_list[2],log_list[4])
                    if tmpo==1:
                        Add_Host_inDB2(log_list[11], log_list[12],log_list[2],log_list[4])
                    if tmpo==2:
                        Add_Host_inDB2(log_list[11], log_list[12],log_list[4],log_list[4])
                '''
                bad_info_pie(log_list[11], log_list[12],log_list[13],log_list[8])
                os.write(handle, (" ".join(log_list)+"\n"))
                os.close(handle)

                log_event_for_web(log_list)
                    #if src_ip not in IP_MAC_IN_LOG and src_ip in IP_MAC_DICT_SS:
                    #    log_event_for_ip_mac(src_ip, log_list[1])
                    #elif dst_ip not in IP_MAC_IN_LOG and dst_ip in IP_MAC_DICT_SS:
                    #    log_event_for_ip_mac(dst_ip, log_list[1])
                    #os.write(handle, event)
            except Exception, ex:
                print(ex)
            except:
                if config.SHOW_DEBUG:
                    traceback.print_exc()

    server = ThreadingUDPServer((address, port), UDPHandler)

    print "[i] running UDP server at '%s:%d'" % (server.server_address[0], server.server_address[1])

    if join:
        server.serve_forever()
    else:
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()

def set_sigterm_handler():
    def handler(signum, frame):
        log_error("SIGTERM")
        raise SystemExit

    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, handler)

if __name__ != "__main__":
    set_sigterm_handler()
