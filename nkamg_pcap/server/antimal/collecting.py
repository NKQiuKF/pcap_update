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
FEEDS = os.path.abspath("trails/feeds")
CUSTOM = os.path.abspath("trails/custom")
STATIC = os.path.abspath("trails/static")

# trails csv
USERS_DIR = os.path.join(os.path.expanduser("~"), ".antimal" )
TRAILS_CSV =os.path.join(USERS_DIR, "trails.csv")
COLUMNS = ["trail", "info", "ref","ftime_new","ltime_new"]


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
    
    list_trails = []
    if not (os.path.isfile('trail_info.csv')): # create a csv for first time of updating
        print "can't find collecting_info.csv! then init a new csv"
        old=pd.read_csv(TRAILS_CSV,names=['trail', 'info', 'ref'])
        old['ftime']=datetime.now().strftime('%Y-%m-%d:%H')
        old['ltime']=datetime.now().strftime('%Y-%m-%d:%H')
        old.to_csv('trail_info.csv', index=False)
    else:
        old=pd.read_csv('trail_info.csv')
    old_trails=set(old.trail)
    print "[i] collecting trails information (ftime,ltime)..."
    
    filenames = sorted(glob.glob(os.path.join(FEEDS, "*.py")))
    filenames = [_ for _ in filenames if "__init__.py" not in _]
    filenames +=sorted(glob.glob(os.path.join(STATIC, "*.py"))) # in static folder, __init__.py has fetch() 
    filenames +=sorted(glob.glob(os.path.join(CUSTOM, "*.py")))# in custom folder, __init__.py has fetch()
    #remove __init__.py in feeds folder
    #filenames = [_ for _ in filenames if "__init__.py" not in _]
    #print filenames
    init_sys_path()
    time=datetime.now().strftime('%Y-%m-%d:%H')
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
                
                results = function()

                for item in results.items():
                    	
                    list_trails.append((item[0], item[1][0],item[1][1],time,time))       
                        
                         
                #except Exception, ex:
                #    print "[x] Failed: process feed file '%s' ('%s')" % (filename, ex)

    if list_trails:
        new = pd.DataFrame(list_trails, columns=COLUMNS)
        new_trails=set(new.trail)
        disappeared_trails=old_trails-new_trails                #append to new_info from old_info
        appeared_trails=new_trails-old_trails               #update ftime and ltime
        again_trails=old_trails & new_trails           #update ltime

        


        appeared_again=pd.merge(old,new,on=['trail','info','ref'])
        appeared_again=appeared_again[['trail',"info", "ref","ftime","ltime_new"]]
        appeared_again=appeared_again.rename(columns={'ltime_new':'ltime'})
        appeared_again= appeared_again.drop_duplicates()
        #appeared_again.to_csv('updated_trails.csv',index=None)

        appeared_new = pd.DataFrame({'trail':list(appeared_trails)})
        appeared_new=pd.merge(appeared_new,new,on='trail')
        appeared_new=appeared_new.rename(columns={'ftime_new':'ftime','ltime_new':'ltime'}) 
        appeared_new= appeared_new.drop_duplicates()
        #appeared_new.to_csv('new_trails.csv',index=None)

        disappeared=pd.DataFrame({'trail':list(disappeared_trails)})
        disappeared=pd.merge(disappeared,old,on='trail')
        disappeared= disappeared.drop_duplicates()
        #disappeared.to_csv('old_trails.csv',index=None)

        total=[appeared_again,appeared_new,disappeared]

        result = pd.concat(total)
        result.to_csv('trail_info.csv',index=None)
   
        
    print "[i]collecting informatio finished!"
    #thread = threading.Timer(7200.0, update_trails)
    #thread.daemon = True
    #thread.start()
def server_call():
    try:
        update_trails()
    except KeyboardInterrupt:
        print "\r[x] Ctrl-C pressed"
def main():
    try:
        update_trails()
    except KeyboardInterrupt:
        print "\r[x] Ctrl-C pressed"

if __name__ == "__main__":

    main()
