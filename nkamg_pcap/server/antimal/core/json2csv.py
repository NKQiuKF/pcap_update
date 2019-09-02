#!/usr/bin/env python

import json
import pandas as pd
import os
import re

#file_csv = "netflow20151222.csv"

DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COLUMNS = []

file_csv = os.path.join(DIR, "data/netflow20151222.csv")
file_json = os.path.join(DIR, "data/netflow20151222.json")



def get_zhao_col(file_json=file_json, file_csv=file_csv):
    """ Print columns """
    with open(file_json, "rb") as _json:
        i = 0
        for _ in _json:
            if _.startswith("index", 2):
                continue
            #_ = json.loads(_)
            _ = _.strip()
            _ = _.replace("{", "")
            _ = _.replace("}", "")
            _ = _.replace("\"", "")
            print _
            _ = re.sub(r':[\d\w.]+' ,"", _)
            print _
            COLUMNS = _.split(",")
            print COLUMNS
            break

def read_zhao_json(file_json=file_json, file_csv=file_csv):
    _csv = open(file_csv, "wb")
    with open(file_json, "rb") as _json:
        i = 0
        for _ in _json:
            if _.startswith("index", 2):
                continue
            _ = _.strip()
            _ = _.replace("{", "")
            _ = _.replace("}", "")
            _ = _.replace("\"", "")
            _ = re.sub(r'[a-z_]+:' ,"", _)
            #print _
            #_l = json.loads(_)
            #print type(_l)
            #print _l["dst_ip"]
            #print _l["dst_port"]
            #print _l["src_ip"]
            #print _l["src_port"]
            #print _l["dst_ip"]
            #print _l["dst_ip"]
            #print _l["dst_ip"]
            #print _l["dst_ip"]
            #print json.loads(_).src_ip
            _csv.write(_)
            #i += 1
            #if i == 5:
            #    break
    print "Total Flows: {}".format(i)
    _csv.close()

def csv_add_col(file_csv=file_csv):
    df = pd.read_csv(file_csv, header=None, names=COLUMNS)
    df.to_csv(file_csv, index_label="id")

if __name__ == "__main__":
    read_zhao_json(file_json, file_csv)
