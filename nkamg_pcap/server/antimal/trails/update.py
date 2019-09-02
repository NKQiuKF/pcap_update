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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# to enable calling from current directory too

# trails folders
FEEDS = os.path.abspath("feeds")
CUSTOM = os.path.abspath("custom")
STATIC = os.path.abspath("static")

# trails csv
TRAILS_CSV = os.path.abspath("./trails.csv")
COLUMNS = ["trail", "info", "ref"]

def init_sys_path():
    sys.path.append(FEEDS)
    sys.path.append(CUSTOM)
    sys.path.append(STATIC)

def update_trails():
    """
    Update trails from feeds
    """
    list_trails = []

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
                    for item in results.items():
                        list_trails.append((item[0], item[1][0], item[1][1]))
                except Exception, ex:
                    print "[x] Failed: process feed file '%s' ('%s')" % (filename, ex)

        try:
            if list_trails:
                df = pd.DataFrame(list_trails, columns=COLUMNS)
                df.to_csv(TRAILS_CSV, index_label="id")

        except Exception, ex:
            print "[x] Failed: write trails file '%s' ('%s')" % (TRAILS_CSV, ex)

    print "[i] update finished!"

def main():
    try:
        update_trails()
    except KeyboardInterrupt:
        print "\r[x] Ctrl-C pressed"

if __name__ == "__main__":
    main()
