#!/bin/bash
while true
do
x=`ps -ef|grep monitor.py|grep -v grep|head -n 1|awk {'print $9'}`
if [ -z "$x" ];then
	./monitor.py &  
	echo start monitor
fi

y=`ps -ef|grep replay.py|grep -v grep|head -n 1|awk {'print $9'}`
if [ -z "$y" ];then
	./replay.py & 
	echo start replay
fi

z=`ps -ef|grep send_syslog.py|grep -v grep|head -n 1|awk {'print $9'}`
if [ -z "$z" ];then
	./send_syslog.py & 
	echo start send_syslog
fi
sleep 60s
done
