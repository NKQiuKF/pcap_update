#!/bin/bash
#备份脚本
source sensor.cfg

HOST=$HOST
USER=$USER
PASS=$PASS
PCAPDIR=$PCAPDIR
interface=$interface

#打包存放的路径
BACKUP=$BACKUP
#FTP服务器上的存放路径
PCAPBACK=$PCAPBACK

rm -f $PCAPDIR/*

tcpdump -i $interface -s0 -G 30 -w ${PCAPDIR}/pcap_"%Y%m%d%H%M%S".pcap &
while true
do
    #tdid=`pgrep tcpdump`
    #sleep 29s
    #判断两个文件是否产生，如果已产生两个文件，则上传第一个
    file=`ls -l $PCAPDIR|grep -v total|head -n 1|awk '{print $9}'`
    newfile=`ls -l $PCAPDIR|grep -v total|tail -n 1|awk '{print $9}'`
    cd $PCAPDIR
    if [[ "$file" != "$newfile" ]];then
    #切换到pcap文件的路径
    TARNAME=${BACKUP}/${file}".tar.gz"
    echo $TARNAME
    #打包数据
    tar -czf ${TARNAME} ${file}  > /dev/null #2>&1
    
#    备份
if [[ "$UPLOAD" = "True" ]];then
ftp -i -n -v <<!
    open ${HOST}
    user ${USER} ${PASS}
    bin
    cd ${PCAPBACK}
    put ${TARNAME}
bye
!

    #删除主服务器的备份文件
	rm -f ${BACKUP}/*.gz
fi
	rm -f $PCAPDIR/$file
	fi
done
