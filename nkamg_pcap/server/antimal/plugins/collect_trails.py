#!/usr/bin/env python

import pandas as pd
import glob
import inspect
import os
import sqlite3
import subprocess
import sys
import time
import urllib
from core.common import load_trails
from core.trailsdict import TrailsDict

from datetime import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# to enable calling from current directory too

# trails folders
FEEDS = os.path.abspath("feeds")
CUSTOM = os.path.abspath("custom")
STATIC = os.path.abspath("static")

# trails csv
USERS_DIR = os.path.join(os.path.expanduser("~"), ".antimal" )
TRAILS_CSV =os.path.join(USERS_DIR, "trails.csv")
COLUMNS = ["trail", "info", "ref","ftime","ltime"]


def init_sys_path():
    sys.path.append(FEEDS)
    sys.path.append(CUSTOM)
    sys.path.append(STATIC)

def update_trails():
    """
    Update trails from feeds
    """
    print datetime.now().strftime('%Y-%m-%d:%H')
    trails = TrailsDict()
    trails.update(load_trails())       #load trails
    '''old=pd.read_csv(TRAILS_CSV,names=['trail', 'info', 'ref'])
    old['ftime']=datetime.now().strftime('%Y-%m-%d:%H')
    old['ltime']=datetime.now().strftime('%Y-%m-%d:%H')
    old.to_csv('old_info.csv',index_label="id")
    exit(1)'''
    list_trails = []
    if not (os.path.isfile('trail_info.csv')): # create a csv for first time of updating
        print "can't find collecting_info.csv!"
        old=pd.read_csv(TRAILS_CSV,names=['trail', 'info', 'ref'])
        old['ftime']=datetime.now().strftime('%Y-%m-%d:%H')
        old['ltime']=datetime.now().strftime('%Y-%m-%d:%H')
        old.to_csv('trail_info.csv',index_label="id")
    else:
        old=pd.read_csv('trail_info.csv')
    old_trails=set(old.trail)
    print "[i] updating trails (this might take a while)..."
    
    filenames = sorted(glob.glob(os.path.join(FEEDS, "*.py")))
    filenames += [STATIC] # in static folder, __init__.py has fetch()
    filenames += [CUSTOM] # in custom folder, __init__.py has fetch()
    # remove __init__.py in feeds folder
    filenames = [_ for _ in filenames if "__init__.py" not in _]

    init_sys_path()
    for i in xrange(len(filenames)):
        f = filenames[i]
        try:
            module = __import__(os.path.basename(f).split(".py")[0])
        except (ImportError, SyntaxError), ex:
            print "[x] Failed: import feed file '%s' ('%s')" % (f, ex)
            continue

        for name, function in inspect.getmembers(module, inspect.isfunction):
            if name == "fetch":
                print "[o] '%s'" % (module.__url__)
                sys.stdout.write("[?] progress: %d/%d (%d%%)\r" % \
                    (i, len(filenames), i * 100 / len(filenames)))
                sys.stdout.flush()
                try:
                    results = function()
                    #print(1)
                    for item in results.items():
                        list_trails.append((item[0], item[1][0],item[1][1],datetime.now().strftime('%Y-%m-%d:%H'),datetime.now().strftime('%Y-%m-%d:%H')))       
                        '''if(item[0] in trails):
                            tmp=str(old[old.trail == item[0]].ftime)
                            list_trails.append((item[0], item[1][0],item[1][1],tmp[5:18],time))
                            #print(1)
                        else:
                         
                            list_trails.append((item[0], item[1][0],item[1][1],time,time))
                        
                         '''
                except Exception, ex:
                    print "[x] Failed: process feed file '%s' ('%s')" % (filename, ex)


    print 'finish!'

    if list_trails:
        new = pd.DataFrame(list_trails, columns=COLUMNS)
        new_trails=set(new.trail)
        disappeared=old_trails-new_trails                #append to new_info from old_info
        appeared_new=new_trails-old_trails               #update ftime and ltime
        appeared_again=old_trails & new_trails           #update ltime
            #exit(0)
            
        for _ in appeared_again:       
            tmp=str(old[old.trail == _].ftime)
            #print tmp[9:22]
            index0=new[new.trail == _].index[0]
            #print id1
            new.loc[index0,'ftime']=tmp[9:22]

        for _ in disappeared:
            tmp_info=str(old[old.trail==_].info)
            tmp_ref=str(old[old.trail==_].ref)
            tmp_ftime=str(old[old.trail==_].ftime)
            tmp_ltime=str(old[old.trail==_].ltime)
            tmp_set=[tmp_info,tmp_ref,tmp_ftime,tmp_ltime]
            new.loc[len(new)]=tmp_set

        new.to_csv('trail_info.csv', index_label="id")

        
    print "[i] update finished!"

def main():
    try:
        update_trails()
    except KeyboardInterrupt:
        print "\r[x] Ctrl-C pressed"

if __name__ == "__main__":

    main()
