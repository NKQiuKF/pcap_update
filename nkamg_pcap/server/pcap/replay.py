#!/usr/bin/env python
#! -*- coding:utf-8 -*-

import os
import ConfigParser
import shutil

config = ConfigParser.ConfigParser()
config.read("config.ini")

PATH_TEMP = config.get("directory","path_temp")
PATH_SYSLOG = config.get("directory","path_syslog")
INTERFACE = config.get("interface","interface")

def move_pcap(x):
  if os.path.exists(PATH_SYSLOG+x): 
    os.remove(PATH_SYSLOG+x)
  shutil.move(x,PATH_SYSLOG)

def main():
  while True:
    path = os.listdir(PATH_TEMP)
    if path:
      pcaps = sorted(path)
      os.chdir(PATH_TEMP)
      len_pcaps = len(pcaps)
      for i in range(1+len_pcaps/1000):
        filelist = str(pcaps[i*1000:(i+1)*1000])[1:-1]
        # [1:-1]: remove '[' and ']'
        # [i*1000:(i+1)*1000]: if the length is less than 1000, it will take all items.
        os.popen("tcpreplay -i " + INTERFACE + " -M 1000 " + filelist)
        map(move_pcap, pcaps[i*1000:(i+1)*1000])
        #如果出现Message too long，则使用ifconfig interface mtu 3000
        #或者设置得更大
        #print "Send "+f

if __name__ == '__main__':
  main()

