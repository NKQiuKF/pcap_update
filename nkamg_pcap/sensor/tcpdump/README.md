# **tcpdump 脚本介绍**



##sensor.cfg

存储配置信息

ftp服务器ip地址，用户名，密码

PCAPDIR：sensor储存pcap的目录

interface：sensor监听的网络接口

BACKUP：sensor储存pcap压缩包的目录

PCAPBACK：ftp服务器储存pcap的目录

SWITCH：控制ftp的开关



##backup.sh

source sensor.cfg		读取配置文件



rm -f $PCAPDIR/*		清空sensor端pcap存储目录



tcpdump -i \$interface -s0 -G 30 -w \${PCAPDIR}/pcap_"%Y%m%d%H%M%S".pcap &

-i interface	设置网络接口

-s 0		设置从数据包中截取字节数，0代表65535字节，数据包会被完整抓取.

不设置则为默认68字节，部分数据包会被截断.

-G 30	设置抓包时间为30s

-w filename	设置输出文件

&			设置进程为后台进程.否则前台进程占据shell，无法进行其他操作.



file=\`ls -l $PCAPDIR|grep -v total|head -n 1|awk '{print $9}'\`

获得 PCAPDIR目录下第一个文件	，newfile为最后文件


if [[ "\$file" != "\$newfile" ]]		实际意义是确定目录是否只有一个pcap，如果只有一个pcap，不能保证该pcap已经被dump完毕。如果出现多个pcap，第一个pcap肯定dump完毕，然后进行压缩、ftp上传.



##cron.sh

x= \`ps -ef|grep backup.sh|grep -v grep|head -n 1|awk {'print $9'}`

如果backup.sh已经运行，x为backup，否则为空.



if [ -z "$x" ]		判断x是否非空，x为空进入then，运行backuo.sh.



## 使用方法

1.更新sensor.cfg配置，注意路径

2.将crontab中内容拷贝到/etc/crontab中

3.sudo /etc/init.d/cron restart 	重启cron服务



