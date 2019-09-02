#!/bin/bash

x=`ps -ef|grep backup.sh|grep -v grep|head -n 1|awk {'print $9'}`
if [ -z "$x" ];then
	./backup.sh &
	echo start backup...
fi
