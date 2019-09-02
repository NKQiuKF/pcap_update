#!/bin/bash
#sed -i "s/whereisyournkamg/whereisyournkamg" feature_importance.pickle
PORT="8088"
SHELL_FOLDER=$(dirname $(readlink -f "$0"))
cd $SHELL_FOLDER

export PYTHONPATH=$SHELL_FOLDER
#PATH=$PATH:~/IDA
#x=`ps -ef|grep genAsmAndBytes.py|grep -v grep|head -n 1|awk {'print $9'}`
#if [ -z "$x" ];then
#  python genAsmAndBytes.py 
#  echo generate Asm and Bytes
#fi
#cd ../server/ml/apk/
#if [ ! -d work ];then
#mkdir work
#fi
p=`ps -ef|grep pcapanalysis.py|grep -v grep|head -n 1|awk {'print $9'}`
if [ -z "$p" ];then
	cd ../server/pcap/
	python pcapanalysis.py &
	echo Start PcapAnalysis...
fi
cd $SHELL_FOLDER
superset/bin/superset runserver -p ${PORT} 



