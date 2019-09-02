#!/bin/bash

x=`ps -ef|grep pcapanalysis.py|grep -v grep|awk {'print $2'}`
if [ -n "$x" ];then
	echo "shutdown pcapanalysis"
	kill -9 "$x"
fi
