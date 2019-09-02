#!/usr/bin/env python
#! -*- coding:utf-8 -*-

import ConfigParser
import shutil
import os 
import sys
import argparse
import gzip

config = ConfigParser.ConfigParser()
config.read("config.ini")

PATH_BACK=config.get("directory","path_back")
PATH_WORK=config.get("directory","path_work")
PATH_TEMP=config.get("directory","path_temp")

def process(x):
  decompress(x)
  move(x)

def decompress(x):
  if os.path.splitext(x)[1] != '.gz':
    return
  os.popen('tar -zxf '+x+' -C '+PATH_TEMP)
  print '[monitor.py]: decompressing ',x	

def move(x):
  if os.path.exists(PATH_BACK+x):
    os.remove(PATH_BACK+x)
  shutil.move(x,PATH_BACK)
  print '[monitor.py]: moving ',x

def main():
  while True:
    path=os.listdir(PATH_WORK)
    if path:	
      map(process, path)

if __name__ == '__main__':
  os.chdir(PATH_WORK)
  main()

