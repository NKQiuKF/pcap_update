#!/bin/bash
x=`ps -ef|grep tcpdump|grep -v grep|awk {'print $2'}`
kill -9 "$x"
y=`ps -ef|grep backup.sh|grep -v grep|awk {'print $2'}`
kill -9 "$z"
