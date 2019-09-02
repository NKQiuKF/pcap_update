#!/bin/bash
x=`ps -ef|grep monitor.py|grep -v grep|awk {'print $2'}`
kill -9 "$x"
y=`ps -ef|grep replay.py|grep -v grep|awk {'print $2'}`
kill -9 "$y"
z=`ps -ef|grep send_syslog.py|grep -v grep|awk {'print $2'}`
kill -9 "$z"
